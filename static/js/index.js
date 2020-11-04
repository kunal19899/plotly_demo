function toBorderDark(id){
    document.getElementById(id).classList.remove('border-danger');
    // console.log("hello");
}

function addMin(){
    var date = new Date(document.getElementById('start_of_startDate').value);
    console.log(date);
    console.log(date.getDate());
    date.setDate(date.getDate() + document.getElementById('periodLength').value);
    console.log(2);
    console.log(date);
    console.log(document.getElementById('start_of_startDate').value);
    document.getElementById('start_of_endDate').min = date;
    console.log(document.getElementById('start_of_endDate').min);
}