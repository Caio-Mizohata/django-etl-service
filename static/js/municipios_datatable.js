const ordenar_tabela = () => {
    $('#tabela-municipios').DataTable({
        "language": {
            "url": "//cdn.datatables.net/plug-ins/1.11.5/i18n/pt-BR.json"
        },
        "order": [[3, "desc"]],
        "pageLength": 25,
        "columnDefs": [
            { "orderable": false, "targets": [0] },
            { "type": "num", "targets": [3] },
            { "className": "text-center", "targets": [2] }
        ]
    });

    document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(function(el) {
        new bootstrap.Tooltip(el);
    });
}

$(document).ready(ordenar_tabela);
