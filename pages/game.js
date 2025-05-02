// --- DOM Elements ---
const outputDiv = document.getElementById('output');
const inputAreaDiv = document.getElementById('input-area');
const scoreSpan = document.getElementById('score');
const turnsSpan = document.getElementById('turns');
const maxTurnsSpan = document.getElementById('max-turns');
const inventoryList = document.getElementById('inventory-list');
const achievementsList = document.getElementById('achievements-list');
const statsList = document.getElementById('stats-list');

// --- Game State Classes (Translation from Python) ---

class Inventory {
    constructor(items = {}) {
        this.items = items; // Use an object for items
        this.capacity = 10; // Capacity is less critical in this text game, but keep it
    }

    addItem(itemName, quantity = 1) {
        if (Object.keys(this.items).length >= this.capacity && !(itemName in this.items)) {
            // Check if adding a new item exceeds capacity (existing items can stack)
             // Capacity check is simplified for text adventure, can be more complex if needed
             // console.warn("Inventory full!"); // Optional: add a message
             return false;
        }
        this.items[itemName] = (this.items[itemName] || 0) + quantity;
        return true;
    }

    removeItem(itemName, quantity = 1) {
        if (itemName in this.items) {
            if (this.items[itemName] >= quantity) {
                this.items[itemName] -= quantity;
                if (this.items[itemName] === 0) {
                    delete this.items[itemName];
                }
                return true;
            }
        }
        return false;
    }

    hasItem(itemName) {
        return itemName in this.items && this.items[itemName] > 0;
    }

    getItems() {
        // Return a copy to prevent external modification
        return { ...this.items };
    }
}

class GameState {
    constructor() {
        this.score = 0;
        this.turns = 0;
        this.maxTurns = 10;
        this.inventory = new Inventory(); // Inventory is an instance of the class
        this.achievements = new Set(); // Use a Set for achievements
        this.characterStats = {
            "health": 100,
            "strength": 10,
            "magic": 5,
            "luck": 5
        };
    }

    // Save state to localStorage
    save() {
        const saveData = {
            score: this.score,
            turns: this.turns,
            maxTurns: this.maxTurns,
            // Store inventory items as a plain object
            inventoryItems: this.inventory.items,
            // Store achievements as an array
            achievements: Array.from(this.achievements),
            characterStats: this.characterStats,
            saveDate: new Date().toISOString()
        };
        localStorage.setItem('arcaneEchoesSave', JSON.stringify(saveData));
    }

    // Load state from localStorage
    static load() {
        const savedData = localStorage.getItem('arcaneEchoesSave');
        if (!savedData) {
            return null; // No save data found
        }
        try {
            const saveData = JSON.parse(savedData);
            const gameState = new GameState();
            gameState.score = saveData.score;
            gameState.turns = saveData.turns;
            gameState.maxTurns = saveData.maxTurns;
            // Create a new Inventory instance and populate it
            gameState.inventory = new Inventory(saveData.inventoryItems || {});
            // Populate the achievements Set
            gameState.achievements = new Set(saveData.achievements || []);
            gameState.characterStats = saveData.characterStats || {
                "health": 100, "strength": 10, "magic": 5, "luck": 5
            }; // Handle potential missing stats
            return gameState;
        } catch (e) {
            console.error("Failed to load game state:", e);
            return null; // Handle potential parsing errors
        }
    }
}

// --- Helper Functions ---

// Simulate print_sleep using async/await and setTimeout
async function displayText(message, colorClass = 'reset-text', sleepDuration = 500) {
    const p = document.createElement('p');
    p.classList.add(colorClass);
    p.innerHTML = message; // Use innerHTML to allow emojis and simple formatting if needed
    outputDiv.appendChild(p);
    outputDiv.scrollTop = outputDiv.scrollHeight; // Auto-scroll to bottom
    await new Promise(resolve => setTimeout(resolve, sleepDuration));
}

// Display current game state in the state area
function updateStateDisplay(gameState) {
    scoreSpan.textContent = gameState.score;
    turnsSpan.textContent = gameState.turns;
    maxTurnsSpan.textContent = gameState.maxTurns;

    // Update Inventory
    inventoryList.innerHTML = ''; // Clear current list
    const items = gameState.inventory.getItems();
    if (Object.keys(items).length === 0) {
        const li = document.createElement('li');
        li.textContent = 'Empty';
        inventoryList.appendChild(li);
    } else {
        for (const item in items) {
            const li = document.createElement('li');
            li.textContent = `- ${item}: ${items[item]}`;
            inventoryList.appendChild(li);
        }
    }

     // Update Achievements
    achievementsList.innerHTML = ''; // Clear current list
    const achievements = Array.from(gameState.achievements);
    if (achievements.length === 0) {
        const li = document.createElement('li');
        li.textContent = 'None yet';
        achievementsList.appendChild(li);
    } else {
        achievements.forEach(achievement => {
            const li = document.createElement('li');
            li.textContent = `- ${achievement}`;
            achievementsList.appendChild(li);
        });
    }

     // Update Stats
    statsList.innerHTML = ''; // Clear current list
    const stats = gameState.characterStats;
    for (const stat in stats) {
         const li = document.createElement('li');
         li.textContent = `${stat.charAt(0).toUpperCase() + stat.slice(1)}: ${stats[stat]}`;
         statsList.appendChild(li);
    }
}

// Get user choice via buttons
async function getUserChoice(choices) {
    inputAreaDiv.innerHTML = ''; // Clear previous input options
    return new Promise(resolve => {
        choices.forEach(choice => {
            const button = document.createElement('button');
            button.textContent = choice.text;
            button.addEventListener('click', () => {
                inputAreaDiv.innerHTML = ''; // Clear buttons after choice
                resolve(choice.value); // Resolve the promise with the chosen value
            });
            inputAreaDiv.appendChild(button);
        });
    });
}

// --- Game Logic Functions (Translation from Python) ---

async function displayWelcome() {
    await displayText("🌟 Welcome to Arcane Echoes! 🌟", 'yellow-text');
    await displayText(
        "You wake up in a mystical forest 🌲🌳, the air shimmering with magic ✨.",
        'green-text'
    );
    await displayText(
        "A glow in the distance catches your eye, but you hear rustling nearby 🐾.",
        'green-text'
    );
    await displayText("Your adventure begins now. Choose wisely!", 'yellow-text');
}

async function handleRiddle(gameState) {
    await displayText("You follow the glowing light to a magical clearing 🌼.", 'green-text');
    await displayText("A wise old wizard 🧙‍♂️ appears, his eyes twinkling with mischief.", 'green-text');
    await displayText("He says, 'Solve my riddle to gain a magical artifact! 🪄'", 'green-text');
    await displayText(
        "Riddle: 'I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?'",
        'yellow-text'
    );

    const choices = [
        { text: "1️⃣ Answer: A ghost 👻.", value: "1" },
        { text: "2️⃣ Answer: An echo 🗣️.", value: "2" },
        { text: "3️⃣ Answer: A bird 🐦.", value: "3" },
    ];

    const riddleChoice = await getUserChoice(choices);

    if (riddleChoice === "2") {
        gameState.score += 50;
        await displayText("'Correct!' the wizard exclaims, handing you a glowing amulet 💎.", 'green-text');
        await displayText("The amulet pulses with power, making you feel invincible.", 'green-text');
        await displayText("You thank the wizard and prepare to continue your quest.", 'green-text');
        gameState.inventory.addItem("amulet");
        gameState.achievements.add("Riddle Master");
        updateStateDisplay(gameState);
        return { success: true, gameState };
    } else {
        gameState.score -= 20;
        await displayText("'Wrong!' the wizard says, his voice cold. The clearing fades.", 'red-text');
        await displayText("Shadow creatures attack from the darkness 🌑!", 'red-text');
        await displayText("You barely escape, wounded and defeated. You lose! 😢", 'red-text');
        updateStateDisplay(gameState);
        return { success: false, gameState };
    }
}

async function handleSquirrelEncounter(gameState) {
    await displayText("A friendly squirrel 🐿️ pops out, chattering excitedly.", 'green-text');
    await displayText("It seems to offer guidance through the forest.", 'green-text');

    const choices = [
        { text: "1️⃣ Follow the squirrel to a sunny meadow 🌞.", value: "1" },
        { text: "2️⃣ Head toward a creepy cave nearby 🕸️.", value: "2" },
        { text: "3️⃣ Decline and explore a riverbank instead 🌊.", value: "3" },
    ];

    const squirrelChoice = await getUserChoice(choices);

    if (squirrelChoice === "1") {
        gameState.score += 50;
        await displayText("The squirrel leads you to a meadow bathed in sunlight.", 'green-text');
        await displayText("You find a hidden treasure chest filled with riches! 🎁", 'green-text');
        await displayText("Gold coins and jewels sparkle in your hands. You win! 🎉", 'green-text');
        gameState.achievements.add("Friend of the Forest");
        updateStateDisplay(gameState);
        return { success: true, gameState };
    } else if (squirrelChoice === "2") {
        gameState.score -= 30;
        await displayText("The cave is dark, with eerie whispers echoing around 👻.", 'red-text');
        await displayText("You stumble in the darkness and fall into a deep pit.", 'red-text');
        await displayText("You lose consciousness. You lose! 😱", 'red-text');
         updateStateDisplay(gameState);
        return { success: false, gameState };
    } else { // choice === "3"
        gameState.score += 40;
        await displayText("At the riverbank, you find a sturdy boat waiting 🚤.", 'green-text');
        await displayText("You sail down the river, arriving at a peaceful village.", 'green-text');
        await displayText("The villagers welcome you warmly. You win! 🥳", 'green-text');
        gameState.achievements.add("River Explorer"); // New achievement based on this path
         updateStateDisplay(gameState);
        return { success: true, gameState };
    }
}


async function handleMonsterEncounter(gameState) {
    await displayText("A monster 🐺 bursts from the bushes, growling fiercely!", 'red-text');
    await displayText("Its eyes glow with menace as it charges toward you!", 'red-text');

    const choices = [
        { text: "1️⃣ Fight the monster with a nearby stick 🪵.", value: "1" },
        { text: "2️⃣ Run away as fast as you can 🏃‍♂️.", value: "2" },
        { text: "3️⃣ Try to hide behind a tree 🌳.", value: "3" },
    ];

    const monsterChoice = await getUserChoice(choices);

    if (monsterChoice === "1") {
        const fightResult = Math.random() < 0.5 ? "win" : "lose"; // 50% chance
        if (fightResult === "win") {
            gameState.score += 60;
            await displayText("You swing the stick with all your might!", 'green-text');
            await displayText("The monster falls, defeated by your bravery! 💪", 'green-text');
            await displayText("You find a map 🗺️ on the monster, leading to a castle.", 'green-text');
            await displayText("At the castle, you're crowned a hero! You win! 👑", 'green-text');
            gameState.achievements.add("Monster Slayer");
            updateStateDisplay(gameState);
            return { success: true, gameState };
        } else {
            gameState.score -= 40;
            await displayText("The monster overpowers you, its claws slashing.", 'red-text');
            await displayText("You collapse, defeated. You lose! 😵", 'red-text');
             updateStateDisplay(gameState);
            return { success: false, gameState };
        }
    } else if (monsterChoice === "2") {
        gameState.score += 30;
        await displayText("You sprint away, heart pounding, and escape! 🏃‍♂️💨", 'green-text');
        await displayText("You stumble upon a friendly village, safe at last.", 'green-text');
        await displayText("The villagers offer you shelter. You win! 🏡", 'green-text');
        gameState.achievements.add("Fleet Foot"); // New achievement
         updateStateDisplay(gameState);
        return { success: true, gameState };
    } else { // choice === "3"
        const hideResult = Math.random() < 0.5 ? "success" : "fail"; // 50% chance
        if (hideResult === "success") {
            gameState.score += 30;
            await displayText("You hide silently behind the tree, holding your breath.", 'green-text');
            await displayText("The monster leaves, and you find a safe path.", 'green-text');
            await displayText("You reach a village and are welcomed. You win! 🥰", 'green-text');
            gameState.achievements.add("Stealthy Survivor"); // New achievement
             updateStateDisplay(gameState);
            return { success: true, gameState };
        } else {
            gameState.score -= 30;
            await displayText("The monster sniffs you out and attacks! 😱", 'red-text');
            await displayText("You try to flee but are overwhelmed. You lose!", 'red-text');
             updateStateDisplay(gameState);
            return { success: false, gameState };
        }
    }
}

async function handleFinalPath(gameState) {
     await displayText("With the amulet's power, you venture deeper into the forest.", 'green-text');
     await displayText("The path splits, presenting a crucial choice:", 'green-text');

     const choices = [
         { text: "1️⃣ A rickety bridge over a roaring river 🌉.", value: "1" },
         { text: "2️⃣ A narrow trail leading to a towering mountain ⛰️.", value: "2" },
     ];

     const finalChoice = await getUserChoice(choices);

     if (finalChoice === "1") {
         const bridgeResult = Math.random() < 0.5 ? "safe" : "break"; // 50% chance
         if (bridgeResult === "safe") {
             gameState.score += 50;
             await displayText("You carefully cross the bridge, which holds strong.", 'green-text');
             await displayText("Beyond lies a grand kingdom, its gates open wide! 🏰", 'green-text');
             await displayText("The king rewards your bravery. You win! 🎊", 'green-text');
             gameState.achievements.add("Bridge Master"); // New achievement
              updateStateDisplay(gameState);
             return { success: true, gameState };
         } else {
             gameState.score -= 40;
             await displayText("The bridge creaks and snaps beneath you!", 'red-text');
             await displayText("You fall into the raging river below. 🌊", 'red-text');
             await displayText("You're swept away, defeated. You lose! 😢", 'red-text');
              updateStateDisplay(gameState);
             return { success: false, gameState };
         }
     } else { // finalChoice === "2"
         gameState.score += 60;
         await displayText("You climb the steep trail, reaching a dragon's lair! 🐉", 'green-text');
         await displayText("The dragon, awed by your amulet, bows respectfully.", 'green-text');
         await displayText("It offers you a hoard of treasure. You win! 💰🎉", 'green-text');
         gameState.achievements.add("Dragon Friend"); // New achievement
          updateStateDisplay(gameState);
         return { success: true, gameState };
     }
 }


async function handleTreasureVault(gameState) {
     await displayText("You stumble upon a hidden vault, its door glowing with runes.", 'green-text');
     await displayText("A magical lock bars your entry, pulsing with energy.", 'green-text');

     const choices = [
         { text: "1️⃣ Try to pick the lock with your skills 🔓.", value: "1" },
         { text: "2️⃣ Search the area for a hidden key 🗝️.", value: "2" },
         { text: "3️⃣ Attempt to cast a spell to unlock it 🪄.", value: "3" },
     ];

     const vaultChoice = await getUserChoice(choices);

     if (vaultChoice === "1") {
         const lockResult = Math.random() < 0.5 ? "success" : "trap"; // 50% chance
         if (lockResult === "success") {
             gameState.score += 70;
             await displayText("Your nimble fingers unlock the vault with a click!", 'green-text');
             await displayText("Inside, you find piles of gold and gems! 💎", 'green-text');
             await displayText("You're now a legend of wealth. You win! 🎉", 'green-text');
             gameState.achievements.add("Master Lockpicker"); // New achievement
              updateStateDisplay(gameState);
             return { success: true, gameState };
         } else {
             gameState.score -= 50;
             await displayText("A trap springs! Darts shoot from the walls! 🏹", 'red-text');
             await displayText("You're wounded and retreat in defeat. You lose! 😢", 'red-text');
              updateStateDisplay(gameState);
             return { success: false, gameState };
         }
     } else if (vaultChoice === "2") {
         gameState.score += 60;
         await displayText("You search carefully and find a golden key hidden nearby.", 'green-text');
         await displayText("The key unlocks the vault, revealing treasures galore!", 'green-text');
         await displayText("You claim the riches and win! 💰", 'green-text');
         gameState.achievements.add("Treasure Hunter");
          updateStateDisplay(gameState);
         return { success: true, gameState };
     } else { // vaultChoice === "3"
         const spellResult = Math.random() < 0.5 ? "success" : "fail"; // 50% chance
         if (spellResult === "success") {
             gameState.score += 80;
             await displayText("Your spell glows brightly, and the lock melts away!", 'green-text');
             await displayText("The vault opens, filled with magical artifacts! 🪄", 'green-text');
             await displayText("You're hailed as a master mage. You win! 🎉", 'green-text');
             gameState.achievements.add("Master Mage"); // New achievement
              updateStateDisplay(gameState);
             return { success: true, gameState };
         } else {
             gameState.score -= 40;
             await displayText("The spell backfires, zapping you with energy! ⚡", 'red-text');
             await displayText("You collapse, defeated by your own magic. You lose!", 'red-text');
              updateStateDisplay(gameState);
             return { success: false, gameState };
         }
     }
}


async function handleGhostlyEncounter(gameState) {
     await displayText("A ghostly figure 👻 materializes, its voice echoing eerily.", 'cyan-text');
     await displayText("It offers a challenge to prove your worth.", 'cyan-text');

     const choices = [
         { text: "1️⃣ Answer its cryptic question.", value: "1" },
         { text: "2️⃣ Offer a tribute to appease it.", value: "2" },
         { text: "3️⃣ Flee from the ghostly presence.", value: "3" },
     ];

     const ghostChoice = await getUserChoice(choices);

     if (ghostChoice === "1") {
         const questionResult = Math.random() < 0.5 ? "correct" : "wrong"; // 50% chance
         if (questionResult === "correct") {
             gameState.score += 65;
             await displayText("You answer wisely: 'The moon guides the lost.'", 'green-text'); // Fixed answer example
             await displayText("The ghost nods and grants you passage to a shrine.", 'green-text');
             await displayText("You're blessed with wisdom. You win! 🌟", 'green-text');
             gameState.achievements.add("Ghost Whisperer");
              updateStateDisplay(gameState);
             return { success: true, gameState };
         } else {
             gameState.score -= 45;
             await displayText("Your answer falters, angering the ghost!", 'red-text');
             await displayText("It curses you, draining your strength. You lose! 😢", 'red-text');
              updateStateDisplay(gameState);
             return { success: false, gameState };
         }
     } else if (ghostChoice === "2") {
         gameState.score += 55;
         await displayText("You offer a shiny trinket, and the ghost accepts.", 'green-text');
         await displayText("It vanishes, leaving a path to a sacred grove.", 'green-text');
         await displayText("You're honored as a peacemaker. You win! 🌿", 'green-text');
         gameState.achievements.add("Peacemaker"); // New achievement
          updateStateDisplay(gameState);
         return { success: true, gameState };
     } else { // ghostChoice === "3"
         const fleeResult = Math.random() < 0.5 ? "escape" : "capture"; // 50% chance
         if (fleeResult === "escape") {
             gameState.score += 35;
             await displayText("You run swiftly, evading the ghost's grasp!", 'green-text');
             await displayText("You find a safe haven in a nearby village.", 'green-text');
             await displayText("You're safe at last. You win! 🏡", 'green-text');
             gameState.achievements.add("Ethereal Escapee"); // New achievement
              updateStateDisplay(gameState);
             return { success: true, gameState };
         } else {
             gameState.score -= 35;
             await displayText("The ghost catches you, its touch freezing!", 'red-text');
             await displayText("You're trapped in its realm. You lose! 👻", 'red-text');
              updateStateDisplay(gameState);
             return { success: false, gameState };
         }
     }
}


// Main game turn logic
async function playGame(gameState) {
    updateStateDisplay(gameState);

    if (gameState.turns >= gameState.maxTurns) {
        await displayText("⏳ Time runs out! The forest's magic fades.", 'red-text');
        await displayText("You're lost in the woods forever. You lose! 😢", 'red-text');
        return { success: false, gameState }; // Indicate game ended
    }

    const choices = [
        { text: "1️⃣ Follow the glowing light to the west 🌅.", value: "1" },
        { text: "2️⃣ Investigate the rustling in the bushes to the east 🐿️.", value: "2" },
        { text: "3️⃣ Explore a faint trail to the north 🛤️.", value: "3" },
    ];

    await displayText(`⏳ You have ${gameState.maxTurns - gameState.turns} turns remaining.`, 'yellow-text');
    const choice = await getUserChoice(choices);

    gameState.turns += 1;
    gameState.score += 10; // Base score for making a choice

    let result = { success: false, gameState: gameState }; // Default result

    if (choice === "1") {
        await displayText("You head toward the glowing light, feeling drawn to it.", 'green-text');
        result = await handleRiddle(gameState);
        if (result.success && gameState.inventory.hasItem("amulet")) { // Only proceed if riddle was solved and amulet gained
             gameState.score += 20; // Bonus for amulet
             await displayText("The amulet guides you to a final challenge.", 'green-text');
             gameState.turns += 1; // Another turn for the final challenge
             updateStateDisplay(gameState); // Update turns display immediately
             if (gameState.turns >= gameState.maxTurns) {
                 await displayText("⏳ Time runs out before you can face the final challenge!", 'red-text');
                 await displayText("You get lost on the way. You lose! 😢", 'red-text');
                 return { success: false, gameState };
             }
             result = await handleFinalPath(gameState);
        }
    } else if (choice === "2") {
        await displayText("You cautiously approach the rustling bushes.", 'green-text');
        const encounter = Math.random() < 0.5 ? "friend" : "monster"; // 50% chance
        if (encounter === "friend") {
            await displayText("The bushes part to reveal a friendly creature!", 'green-text');
            result = await handleSquirrelEncounter(gameState);
        } else {
            await displayText("A terrifying roar echoes from the bushes!", 'red-text');
            result = await handleMonsterEncounter(gameState);
        }
    } else { // choice === "3"
        await displayText("You follow the faint trail, curious about its secrets.", 'green-text');
         const encounter = Math.random() < 0.5 ? "vault" : "ghost"; // 50% chance
         if (encounter === "vault") {
             await displayText("The trail leads to a mysterious structure!", 'green-text');
             result = await handleTreasureVault(gameState);
         } else {
             await displayText("A chill runs down your spine as the air grows cold.", 'cyan-text');
             result = await handleGhostlyEncounter(gameState);
         }
    }

    updateStateDisplay(gameState); // Update state after encounter

    // Return the outcome and updated game state
    return result;
}


// --- Main Game Loop ---

async function main() {
    await displayText("Welcome to Arcane Echoes! 🎮", 'yellow-text');

    let gameState = GameState.load();

    if (gameState) {
        await displayText("A saved game was found. Would you like to load it?", 'yellow-text', 0); // No sleep for quick prompt
        const loadChoice = await getUserChoice([{ text: "Yes", value: "yes" }, { text: "No", value: "no" }]);

        if (loadChoice === "yes") {
            await displayText("Game loaded successfully! 🎮", 'green-text');
        } else {
            gameState = new GameState();
            await displayText("Starting a new game! 🎮", 'green-text');
             // Clear localStorage if starting new game explicitly after being prompted
            localStorage.removeItem('arcaneEchoesSave');
        }
    } else {
        gameState = new GameState();
        await displayText("Starting a new game! 🎮", 'green-text');
    }

    let gameResult = { success: false, gameState: gameState }; // To hold the outcome of the game turn

    // The main game loop runs only once per "play session" in this structure,
    // as playGame handles the main turn sequence until win/loss/turns run out.
    // The post-game menu then determines if playGame is called again (new game).
    gameResult = await playGame(gameState);

    // Display the game outcome
    if (gameResult.success) {
        await displayText(`🎮 Game Over! You won 🎉. Your score: ${gameResult.gameState.score}, Turns taken: ${gameResult.gameState.turns}`, 'win-text');
    } else {
        await displayText(`🎮 Game Over! You lost 😢. Your score: ${gameResult.gameState.score}, Turns taken: ${gameResult.gameState.turns}`, 'lose-text');
    }


    // Post-game menu
    while (true) {
        await displayText("\nWhat would you like to do?", 'yellow-text', 500);
        const postGameChoices = [
            { text: "1️⃣ Play again", value: "1" },
            { text: "2️⃣ Save game", value: "2" },
            { text: "3️⃣ Quit", value: "3" },
        ];
        const choice = await getUserChoice(postGameChoices);

        if (choice === "1") {
             // Clear output and reset state display for a new game
            outputDiv.innerHTML = '';
            gameState = new GameState(); // Reset for new game
            updateStateDisplay(gameState);
            await displayText("\n" + "🌟".repeat(15) + "\n", 'yellow-text'); // Separator
            await displayText("A new quest awaits you!", 'yellow-text');
             // Rerun the main game turn logic for the new game
             gameResult = await playGame(gameState);
             if (gameResult.success) {
                 await displayText(`🎮 Game Over! You won 🎉. Your score: ${gameResult.gameState.score}, Turns taken: ${gameResult.gameState.turns}`, 'win-text');
             } else {
                 await displayText(`🎮 Game Over! You lost 😢. Your score: ${gameResult.gameState.score}, Turns taken: ${gameResult.gameState.turns}`, 'lose-text');
             }
        } else if (choice === "2") {
            gameState.save();
            await displayText("Game saved successfully! 💾", 'green-text');
            await displayText("Thanks for playing! Come back for another adventure! 👋", 'yellow-text');
            break; // Exit the post-game loop
        } else { // choice === "3"
            await displayText("Thanks for playing! Come back for another adventure! 👋", 'yellow-text');
             // Optional: Clear save on quit if it wasn't explicitly saved
             // localStorage.removeItem('arcaneEchoesSave');
            break; // Exit the post-game loop
        }
    }
}

// --- Start the game when the DOM is fully loaded ---
document.addEventListener('DOMContentLoaded', main);