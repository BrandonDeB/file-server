import DiceBox from '@3d-dice/dice-box-threejs';
let rollers = new Map();

const colors = [
   "#00ffcb",
   "#ff6600",
   "#1d66af",
   "#7028ed",
   "#c4c427",
   "#d81128"
];


const rollBtn = document.getElementById("rollBtn");
const rollInp = document.getElementById("rollinput");
const rollArea = document.getElementById("roll-area");
const currentUser = JSON.parse(document.getElementById("user").textContent);
console.log(currentUser);
document.querySelector('#rollBtn').onclick = function(e) {
  const randomColor = colors[Math.floor(Math.random() * colors.length)];

  rollers.get(currentUser).updateConfig({
    theme_customColorset: {
      background: randomColor,
      foreground: "#ffffff",
      material: "metal"
    }
  });

  rollers.get(currentUser).roll(
    rollInp.value
  );
};


const roomId = JSON.parse(document.getElementById("roomcode").textContent);

const roomSocket = new WebSocket(
   'ws://'
   + window.location.host
   + '/ws/rooms/'
   + roomId
   + '/'
);

roomSocket.onmessage = function(e) {
   const data = JSON.parse(e.data);
   if (data.type == "roll") {
      console.log("Someone rolled the dice");
      //ROLL THE DICE
      if (currentUser == data.user) {
         return;
      }
      let notation = data.results.notation;
      const sets = data.results.sets;
      console.log("Sets:" + sets.join(","));
      let rolls = []
      for (const set of sets) {
         for (const roll of set.rolls) {
            rolls.push(roll.value);
         }
      }
      notation += "@" + rolls.join(",");
      console.log(notation);
      rollers.get(data.user).roll(notation);
   } else if (data.type == "load.users") {
      const userList = document.getElementById("user-list");
      const rollerSpace = document.getElementById("roll-area"); 
      rollerSpace.innerHTML = "";
      userList.innerHTML = ""; 
      console.log(data.users);

      rollers = new Map();
      data.users.forEach((user, index) => {
         const li = document.createElement("li");
         const ua = document.createElement("div");
         ua.id = user+"-roll-area";
         ua.className = "single-roller";
         li.textContent = user;
         li.id = user+"-list-item";
         if (!document.getElementById(li.id)) {
            userList.appendChild(li);
            rollArea.appendChild(ua);
            const Box = new DiceBox("#"+ua.id, {
              theme_customColorset: {
                background: "#00ffcb",
                foreground: "#ffffff",
                material: "metal" // metal | glass | plastic | wood
              },
              light_intensity: 1,
              gravity_multiplier: 400,
              baseScale: 60,
              strength: 5,
              onRollComplete: (results) => {
                console.log(`I've got results :>> `, results);
                  if (currentUser == user) {
                     roomSocket.send(JSON.stringify({
                        "user": user,
                        "results": results
                     }));
                  }
              }
            });

            Box.initialize();
            rollers.set(user, Box);
         }
      });
      
   }
}

roomSocket.onclose = function(e) {
   console.error('Socket closed');
}
