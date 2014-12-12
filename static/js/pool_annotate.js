$(document).ready(function() {

function send_annotation(instance_id, value) {
  var args = {
    instance_id: instance_id,
    value: value
  };
  $.ajax($.urls.annotate_instance, {
    data: args,
    success: function(data) {
    },
    error: function(xhr, status, error) {
      alert(error);
    }
  });
}

$('#pool-instances input[type="radio"]').change(function() {
  var instance_id = $(this).parent().parent().attr('instance');
  var value = $(this).val();
  send_annotation(instance_id, value);
});

var current_instance = 0;
var num_instances = $('.instance').length;

function moveCurrentInstance(amount) {
  current_instance += amount;
  if (current_instance < 0) current_instance = 0;
  if (current_instance >= num_instances) current_instance = num_instances - 1;
  $('.active-annotation').removeClass('active-annotation');
  $('.instance').eq(current_instance).addClass('active-annotation');
}

function getCurrentInstanceId() {
  return $('.instance').eq(current_instance).attr('instance');
}

function updateCurrentAnnotation(value) {
  var instance_id = getCurrentInstanceId();
  send_annotation(instance_id, value);
  $('input[name="annotation:' + instance_id + '"][value="' + value + '"]').attr('checked', true);
}

$(document).keyup(function(event) {
  if (event.keyCode == 74) moveCurrentInstance(1);
  if (event.keyCode == 75) moveCurrentInstance(-1);
  if (event.keyCode == 89) {
    updateCurrentAnnotation("correct");
    moveCurrentInstance(1);
  }
  if (event.keyCode == 78) {
    updateCurrentAnnotation("incorrect");
    moveCurrentInstance(1);
  }
  if (event.keyCode == 77) {
    updateCurrentAnnotation("maybe");
    moveCurrentInstance(1);
  }
});

});
