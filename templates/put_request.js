class StravaCommand {
    constructor ( // parameters
        username, apiKey, authenticationKey,
        weekly_mile_goal, weekly_calorie_goal,
        monthly_mile_goal, monthly_calorie_goal ) {

    // nested parameters under property layer of e.g. auth_data
        this.auth_data = {username, apiKey, authenticationKey};
        this.weekly_goals = {weekly_mile_goal, weekly_calorie_goal};
        this.monthly_goals = {monthly_mile_goal, monthly_calorie_goal};
    }
    // StravaCommand methods go here

}

const sendValue = (ev)=> {
    ev.preventDefault();

    let newval = new StravaCommand(
        username = document.getElementById('username').value,
        apiKey = document.getElementById('apiKey').value,
        authenticationKey = document.getElementById('authenticationKey').value,
        weekly_mile_goal = document.getElementById('weekly_mile_goal').value,
        weekly_calorie_goal = document.getElementById('weekly_calorie_goal').value,
        monthly_mile_goal = document.getElementById('monthly_mile_goal').value,
        monthly_calorie_goal = document.getElementById('monthly_calorie_goal').value
    );

    document.getElementById('myForm').reset();

    console.log('sent', newval );
    //https://127.0.0.1:5000
    const Url='https://127.0.0.1:5000';
    axios({
        method:'put',
        url: Url,
        data: {
            newval
        }
    })
    .then(data=>console.log(data))
    .catch(err=> console.log(err))
}

document.addEventListener('DOMContentLoaded', ()=> {
    document.getElementById('btn').addEventListener('click', sendValue);
    });

/*
//XHTTP CALL TO BACKEND REST API
//WHERE TO SEND post to rest api

class AuthenticationData {
    constructor ( username, apiKey, authenticationKey ) {
        this.username = username;
        this.apiKey = apiKey;
        this.authenticationKey = authenticationKey;
    }
}
myAuthenticationDataFunc = (e) => {
    e.preventDefault();

    username = document.getElementById('username');
    apiKey = document.getElementById('apiKey');
    authenticationKey = document.getElementById('authenticationKey');

}

class StravaGoals {
    constructor(mile_goal, calorie_goal) {
        this.mile_goal = mile_goal;
        this.calorie_goal = calorie_goal;
    }
}
myStravaGoalsFunc = (e) => {
    e.preventDefault();

    mile_goal = document.getElementById('mile_goal');
    calorie_goal = document.getElementById('calorie_goal');

}

class StravaCurrentData {
    constructor(current_miles, current_calories) {
        this.current_miles = current_miles;
        this.current_calories = current_calories;
    }
}
myStravaCurrentDataFunc = (e) => {
    e.preventDefault();

    current_miles = document.getElementById('current_miles');
    current_calories = document.getElementById('current_calories');
}

class StravaPeriodData {
    constructor(mile_goal, calorie_goal, current_miles, current_calories) {
        this.mile_goal = mile_goal;
        this.calorie_goal = calorie_goal;
        this.current_miles = current_miles;
        this.current_calories = current_calories;
    }
}
myStravaPeriodDataFunc = (e) => {
    e.preventDefault();

    mile_goal = document.getElementById('mile_goal');
    calorie_goal = document.getElementById('calorie_goal');
    current_miles = document.getElementById('current_miles');
    current_calories = document.getElementById('current_calories');
}

class StravaTotalData {
    constructor(total_miles, total_calories) {
        this.total_miles = total_miles;
        this.total_calories = total_calories;
    }
}

myStravaTotalDataFunc = (e) => {
    e.preventDefault();

    total_miles = document.getElementById('total_miles');
    total_calories = document.getElementById('total_calories');
}
*/