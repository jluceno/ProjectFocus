function get_data() {
    fetch('/update')
      .then(function (response) {
          return response.json();
      }).then(function (text) {
          console.log('GET response:');
          console.log(text.greeting); 

          var test = document.getElementById("cur_weekly_miles");
          test.innerHTML = text.greeting;
      });
}