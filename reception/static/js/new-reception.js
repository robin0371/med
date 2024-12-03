// JS-шаблон создания новой карточки приема к врачу

$('#id_date').on('blur', function(event) {
    var date = event.target.value,
        doctor_id = $('#id_doctor').val();

    if(date && doctor_id){
        getFreeTimeChoices(doctor_id, date)
    }
});


$('#id_doctor').on('change', function(event) {
    var doctor_id = event.target.value,
        date = $('#id_date').val();

    if(date && doctor_id){
        getFreeTimeChoices(doctor_id, date)
    }
});


// Отправляет запрос за свободным рабочим временем врача в конкретный день
function getFreeTimeChoices(doctor_id, date) {
    $.get(
        "/reception/get-free-time-choices",
        {
            doctor_id: doctor_id,
            date: date
        },
        setFreeTimeChoices
    );

    // Заново заполняет поле выбора времени приема свободными значениями времени врача
    function setFreeTimeChoices(data) {
        $("#id_time").empty();

        $(data.free_time).each(function (i) {
            var value = data.free_time[i][0],
                text = data.free_time[i][1];
            $("#id_time").append($('<option></option>').val(value).html(text));
        });
    }
}
