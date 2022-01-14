function displayUploaded_file(e) {
    var uploadButton = document.getElementById('new_user_file');
    var fileName = uploadButton.files[0].name
    console.log(fileName)
    var label = document.getElementById("fileName");
    label.innerText = fileName;
}
function getUsernameAndPassword() {
    var username = document.querySelector('input[name="username"]').value;
    var password = document.querySelector('input[name="password"]').value;
    return { username, password };
}

function postData(url, data) {
    return fetch(url, {
        method: 'POST',
        body: data,
    })
        .then(res => console.log(res))
}

function validateForm(fileName) {
    var usernameAndPassword = getUsernameAndPassword();
    if (usernameAndPassword.username === "" || usernameAndPassword.password === "") {
        setError("Please enter a username and password");
        return false;
    }
    var file = document.getElementById(fileName);
    if (file.files.length === 0) {
        setError("No file selected")
        return false;
    }
    return true;
}

function handleSubmit(event, targetId, url, fileName) {
    loading()
    setError("")
    var formData = new FormData(
        document.getElementById(targetId)
    );

    var uploadButton = document.getElementById(fileName);
    if (!uploadButton.files.length) {
        setError("No file selected")
        loadingDone();
        return;
    }
    formData.append(fileName, uploadButton.files[0]);

    var usernameAndPassword = getUsernameAndPassword();
    if (usernameAndPassword.username === "" || usernameAndPassword.password === "") {
        setError("Please enter a username and password");
        loadingDone();
        return;
    }

    formData.append('username', usernameAndPassword.username);
    formData.append('password', usernameAndPassword.password);


    fetch(url, {
        method: 'POST',
        body: formData,
    })
        .then(res => res.json())
        .then((data) => {
            populateUserCount(data.user_count);
            populateTable(data.user_results);
        })
        .catch(setError)
        .finally(loadingDone)
}

function setError(error) {
    var errorElement = document.getElementById('error');
    errorElement.innerText = error;
}

function populateUserCount(userCount) {
    var userCountElement = document.getElementById('user-count');
    var userCounter = document.createElement('h4');
    userCounter.innerText = `${userCount} users added`;
    userCountElement.appendChild(userCounter);
}

function populateTable(data) {
    console.log(data)
    var table = document.createElement('table');
    var thead = document.createElement('thead');

    var headerRow = document.createElement('tr');
    var userInfoHeader = document.createElement('th');
    var statusInfoHeader = document.createElement('th');
    userInfoHeader.innerText = 'User info';
    statusInfoHeader.innerText = 'Status';
    headerRow.appendChild(userInfoHeader);
    headerRow.appendChild(statusInfoHeader);

    thead.appendChild(headerRow);
    var tbody = document.createElement('tbody');


    data.forEach(function (user) {
        var tr = document.createElement('tr');
        var userInfo = document.createElement('td');
        var statusInfo = document.createElement('td');
        userInfo.innerText = user.details;
        statusInfo.innerText = user.status;
        tr.appendChild(userInfo);
        tr.appendChild(statusInfo);
        if (user.status === "success") {
            tr.classList.add("green")
        }
        if (user.status === "already in course") {
            tr.classList.add("yellow")
        }
        if (user.status.includes("ERROR")) {
            tr.classList.add("red")
        }
        tbody.appendChild(tr);
    });

    table.appendChild(thead);
    table.appendChild(tbody);
    document.getElementById('table-wrapper').appendChild(table);
    document.body.appendChild(table);
}

function loading() {
    var loading = document.getElementById('loading');
    loading.style.display = "block";
}

function loadingDone() {
    var loading = document.getElementById('loading');
    loading.style.display = "none";
}

async function getCourses() {
    const formData = new FormData();
    const usernameAndPassword = getUsernameAndPassword();
    const { username, password } = usernameAndPassword;
    if (!username.length || !password.length) {
        setError("Please enter a username and password");
        loadingDone();
        return;
    }

    formData.append('username', username);
    formData.append('password', password);
    const res = await fetch('/courses', {
        method: 'POST',
        body: formData,
    });
    const data = await res.json();
    console.log(data)
    return data;
}

function populateCourses(courses) {
    var courseSelect = document.getElementById('course-select');
    courses.forEach(function (course) {
        var option = document.createElement('option');
        option.innerText = course.name;
        option.value = course.id;
        courseSelect.appendChild(option);
    });
}



document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('form#enroll').addEventListener('submit', (e) => {
        e.preventDefault();handleSubmit(e, 'enroll', "/users", "new_user_file") 
    });
    document.querySelector("#new_user_file").addEventListener('change', (e) => {
        e.eventPhase === 2 ? displayUploaded_file(e) : null
    });
    document.querySelector("#refresh-courses").addEventListener('click', async (e) => {
        e.preventDefault();
        const data = await getCourses()
        populateCourses(data.courses)
    });
    loadingDone();
});