function pictureChange(value) {
    // var timePeriod = document.getElementById('timePeriod');
    // var selectedValue = select
    if (value == 0){
        path = "dashboard-images/US-Mainland/Map.png";
    }
    else{
        path = "dashboard-images/US-Mainland/P" + value + ".png";
    }
    console.log(path);
    document.getElementById("map").src=path;
}