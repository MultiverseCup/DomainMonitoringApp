from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Domain
from .forms import DomainForm
import whois
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


@login_required
def delete_domain(request, pk):
    """Удаление домена"""
    domain = get_object_or_404(Domain, pk=pk, user=request.user)

    if request.method == 'POST':
        domain_name = domain.name
        domain.delete()
        messages.success(request, f'Домен {domain_name} удален')

        # Если это AJAX запрос, возвращаем JSON
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True})

        return redirect('domain_list')

    # Если GET запрос - показываем страницу подтверждения
    return render(request, 'domains/confirm_delete.html', {'domain': domain})


@login_required
def domain_list(request):
    domains = Domain.objects.filter(user=request.user)

    # Обновляем дни для каждого домена
    for domain in domains:
        domain.update_days_left()

    # Сортируем по дням (ближайшие к истечению первыми)
    domains = domains.order_by('days_left')

    # Считаем статистику
    stats = {
        'total': domains.count(),
        'expiring_soon': domains.filter(days_left__lte=30).count(),
        'critical': domains.filter(days_left__lte=7).count(),
    }

    return render(request, 'domains/list.html', {
        'domains': domains,
        'stats': stats
    })


@login_required
def add_domain(request):
    if request.method == 'POST':
        form = DomainForm(request.POST)
        if form.is_valid():
            domain = form.save(commit=False)
            domain.user = request.user

            # Если не указана дата окончания, пытаемся получить через WHOIS
            if not domain.expiration_date:
                try:
                    import whois
                    from datetime import datetime

                    w = whois.whois(domain.name)
                    if w.expiration_date:
                        if isinstance(w.expiration_date, list):
                            expiration_date = w.expiration_date[0]
                        else:
                            expiration_date = w.expiration_date

                        if isinstance(expiration_date, datetime):
                            domain.expiration_date = expiration_date.date()
                        else:
                            # Пробуем преобразовать строку в дату
                            try:
                                domain.expiration_date = datetime.strptime(str(expiration_date), '%Y-%m-%d').date()
                            except:
                                pass

                    # Получаем регистратора
                    if w.registrar:
                        domain.registrar = w.registrar

                except Exception as e:
                    # Если WHOIS не сработал, оставляем поля как есть
                    pass

            # Сохраняем домен
            domain.save()

            # Обновляем days_left
            domain.update_days_left()

            messages.success(request, f'Домен {domain.name} успешно добавлен!')
            return redirect('domain_list')
    else:
        form = DomainForm()

    return render(request, 'domains/add.html', {'form': form})