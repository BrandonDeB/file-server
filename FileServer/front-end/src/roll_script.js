import DiceBox from '@3d-dice/dice-box-threejs';
// set configurations when invoking the class
const Box = new DiceBox("#roll-area", {
  theme_customColorset: {
    background: "#00ffcb",
    foreground: "#ffffff",
    material: "metal" // metal | glass | plastic | wood
  },
  light_intensity: 1,
  gravity_multiplier: 600,
  baseScale: 100,
  strength: 2,
  onRollComplete: (results) => {
    console.log(`I've got results :>> `, results);
  }
});

console.log("Hello World!");

Box.initialize();

const rollBtn = document.getElementById("rollBtn");
document.querySelector('#rollBtn').onclick = function(e) {
  // dynamically update the dice theme on each roll
  const colors = [
    "#00ffcb",
    "#ff6600",
    "#1d66af",
    "#7028ed",
    "#c4c427",
    "#d81128"
  ];
  const randomColor = colors[Math.floor(Math.random() * colors.length)];

  // all dice will produce the same value picked from the values list randomly
  const values = [1, 2, 3, 4, 5, 6];
  const randomVal = values[Math.floor(Math.random() * values.length)];

  Box.updateConfig({
    theme_customColorset: {
      background: randomColor,
      foreground: "#ffffff",
      material: "metal" // metal | glass | plastic | wood
    }
  });
  Box.roll(
    `7d6@${randomVal},${randomVal},${randomVal},${randomVal},${randomVal},${randomVal},${randomVal}`
  );
};
