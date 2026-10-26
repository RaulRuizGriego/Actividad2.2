from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Cita, Paciente


def inicio(request):
    pendientes = Cita.objects.select_related("paciente").filter(estado=Cita.PENDIENTE)
    contexto = {
        "total_pacientes": Paciente.objects.count(),
        "total_citas": Cita.objects.count(),
        "total_pendientes": pendientes.count(),
        "total_confirmadas": Cita.objects.filter(estado=Cita.CONFIRMADA).count(),
        "proximas": pendientes[:3],
    }
    return render(request, "citas/inicio.html", contexto)


def lista_pacientes(request):
    q = request.GET.get("q", "").strip()
    pacientes = Paciente.objects.all()
    if q:
        pacientes = pacientes.filter(Q(nombre__icontains=q) | Q(apellido__icontains=q))
    return render(
        request, "citas/pacientes_lista.html", {"pacientes": pacientes, "q": q}
    )


def detalle_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    citas = paciente.citas.all()
    return render(
        request,
        "citas/paciente_detalle.html",
        {"paciente": paciente, "citas": citas},
    )


def lista_citas(request):
    citas = Cita.objects.select_related("paciente").all()
    return render(
        request,
        "citas/citas_lista.html",
        {
            "citas": citas,
            "titulo": "Agenda general",
            "descripcion": "Todas las citas programadas, agrupadas por día.",
        },
    )


def citas_pendientes(request):
    citas = Cita.objects.select_related("paciente").filter(estado=Cita.PENDIENTE)
    return render(
        request,
        "citas/citas_lista.html",
        {
            "citas": citas,
            "titulo": "Citas pendientes",
            "descripcion": "Citas que aún esperan confirmación.",
        },
    )
