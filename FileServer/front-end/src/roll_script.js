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
const userList = document.getElementById("user-list");
const rollerSpace = document.getElementById("roll-area"); 

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

function getRollAreaId(user) {
   return `${user}-roll-area`;
}

function createDiceBox(user) {
   return new DiceBox(`#${getRollAreaId(user)}`, {
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
         if (currentUser == user) {
            roomSocket.send(JSON.stringify({
               "user": user,
               "results": results
            }));
         }
         document.getElementById(`${user}-popup-text`).textContent = `${results.notation}=${results.total}`;
         document.getElementById(`${user}-popup`).style.display = "block";
      }
   });

}

function createPopup(user) {
   const popup = document.createElement("div");
   const closeButton = document.createElement("span");
   const popupText = document.createElement("p");
   popup.className = "popup";
   popup.id = `${user}-popup`;
   popup.style.display = "none";
   popupText.id = `${user}-popup-text`;
   closeButton.className = "close-btn";
   closeButton.textContent = "×";
   closeButton.onclick = () => {
      popup.style.display = "none";
   }

   popup.appendChild(closeButton);
   popup.appendChild(popupText);

   return popup;
}

function createDiceObjects(users) {
   rollers = new Map();
   users.forEach((user, index) => {
      const li = document.createElement("li");
      const ua = document.createElement("div");
      const name = document.createElement("h3");
      name.textContent = user;
      name.className = "player-label";
      ua.id = getRollAreaId(user);
      ua.className = "single-roller";
      li.textContent = user;
      li.id = user+"-list-item";
      if (!document.getElementById(li.id)) {
         ua.appendChild(createPopup(user));
         ua.appendChild(name);
         userList.appendChild(li);
         rollArea.appendChild(ua);
         const Box = createDiceBox(user);
         Box.initialize();
         rollers.set(user, Box);
      }
   });
}

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
      if (currentUser == data.user) {
         return;
      }
      let notation = data.results.notation;
      const sets = data.results.sets;
      let rolls = []
      for (const set of sets) {
         for (const roll of set.rolls) {
            rolls.push(roll.value);
         }
      }
      notation += "@" + rolls.join(",");
      rollers.get(data.user).roll(notation);
   } else if (data.type == "load.users") {
      rollerSpace.innerHTML = "";
      userList.innerHTML = ""; 

      createDiceObjects(data.users);
   }
}

roomSocket.onclose = function(e) {
   console.error('Socket closed');
}
