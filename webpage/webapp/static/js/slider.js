function updateValue(value) {
    console.log("belepett")
    document.getElementById('slider-value').innerText = value;
    
    fetch("/slider-endpoint/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify({ slider_value: value })
    }).then(response => response.json())
      .then(data => {
          console.log('Server response:', data);
      }).catch(error => {
          console.error('Error:', error);
      });
}
