require("dotenv").config();

const successEmoji: string = process.env.EMOJI_POS != undefined ? process.env.EMOJI_POS : "";
const failureEmoji: string = process.env.EMOJI_NEG != undefined ? process.env.EMOJI_NEG : "";

const roll = (msg: string): string => {
    const msgComponents: string[] = msg.split(" ").splice(1);
    const diceResult: number[] = diceRoll(msgComponents[0]);
    const diceSum: number = diceResult.reduce((previous, current) => previous + current, 0);
    const restOfArray: string[] = msgComponents.slice(1);
    const finalResult: number = calculateRest(diceSum, restOfArray);
    if (msgComponents.length == 1) {
        if (diceResult.length == 1 && diceResult[0] == 1) {
            return `${failureEmoji} Juu thruu shit **${finalResult}!** ${failureEmoji}`
        } else if (diceResult.length == 1 && diceResult[0] == 20) {
            return `${successEmoji} **Se on natural ${diceResult[0]}! ${successEmoji}**`;
        } else if (diceResult.length != 1) {
            return `Noppien tulos on **${finalResult}**! Sinä heitit **${diceResult.join(", ")}!**`
        } else {
            return `Nopanheittosi tulos on **${finalResult}**!`;
        }
    } else {
        if (diceResult.includes(20)) {
            return `${successEmoji} **Se on natural ${diceResult[0]}!** ${successEmoji}, mutta yhdistetty tulos on **${finalResult}**!`
        } else if (diceResult.includes(1)) {
            return `${failureEmoji} Juu thruu shit **${diceResult[0]}!** ${failureEmoji}, mutta yhdistetty tulos on **${finalResult}**!`
        } else {
            return `Kokonaistulos on **${finalResult}**! Sinä heitit **${diceResult.join(", ")}!**`
        }
    }
}

const diceRoll = (dice: string): number[] => {
    let diceComponents: string[] = dice.split("d");
    let multiplier: number;
    multiplier = (diceComponents[0] != "") ? +diceComponents[0] : 1
    const diceType: number = +diceComponents[1];
    return calculateRoll(multiplier, diceType);
}

const calculateRoll = (multiplier: number, diceType: number): number[] => {
    let rolls: number[] = [];
    for (let i = 0; i < multiplier; i++) {
        rolls.push(Math.floor(Math.random() * diceType + 1));
    }
    return rolls;
}

const calculateRest = (diceSum: number, restOfArray: string[]): number => {
    let sum: number = diceSum;
    for (let i = 0; i < restOfArray.length; i++) {
        if (restOfArray[i] == "+") {
            sum += +restOfArray[i + 1];
        } else if (restOfArray[i] == "-") {
            sum -= +restOfArray[i + 1];
        }
    }
    return sum;
}

export default roll;