async function loadMessages(){

const response = await fetch("http://127.0.0.1:5000/messages")

const data = await response.json()

const table = document.querySelector("#messagesTable tbody")

data.forEach(msg => {

const row = `
<tr>
<td>${msg.id}</td>
<td>${msg.name}</td>
<td>${msg.email}</td>
<td>${msg.message}</td>
</tr>
`

table.innerHTML += row

})

}

loadMessages()