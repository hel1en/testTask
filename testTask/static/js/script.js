function deleteUser(user_id){
		fetch(`http://localhost:8080/api/employees/${user_id}`, {method: 'delete'})
				.then(function (response) {
					// The API call was successful!
					return response.json();
				}).then(function (data) {
					// This is the JSON from our response
					console.log(data);
					return true;
				}).catch(function (err) {
					// There was an error
					console.warn('Something went wrong.', err);
				});

}


function patchUser(){
	const formData = new FormData(document.getElementById('form'))
	let body = {}
	for (const [key, value] of formData){
		body[key] = value
	}
	alert(body['uid'])
	fetch(`http://localhost:8080/api/employees/${body['uid']}`,
		{method: 'PATCH', body: JSON.stringify(body)})
		.then(function (response) {
			// The API call was successful!
			return response.json();
		}).then(function (data) {
			// This is the JSON from our response
			console.log(data);
			return true;
		}).catch(function (err) {
			// There was an error
			console.warn('Something went wrong.', err);
		});

}


function getUsers(){
		fetch('http://localhost:8080/api/employees')
		.then(function (response) {
			// The API call was successful!
			return response.json();
		}).then(function (data) {
			// This is the JSON from our response
			console.log(data);
			let b = document.getElementById('userInfo');
			for (let user of data){
			let c = b.cloneNode()
				c.innerHTML = b.innerHTML.replace(/{UID}/g, user['uid'])
										.replace(/{NAME}/g, user['name'])
										.replace(/{SALARY}/g, user['salary'])
										.replace(/{BOSS}/g, user['boss'])
										.replace(/{POSITION_ID}/g, user['position_key']);
				 document.getElementById('usersBlock').append(c)
				c.hidden = false
			}

			return true;
		}).catch(function (err) {
			// There was an error
			console.warn('Something went wrong.', err);
		});
}

function setPatchFormUserId(user_id){
	document.getElementById("uidToChange").setAttribute("value", user_id)
}