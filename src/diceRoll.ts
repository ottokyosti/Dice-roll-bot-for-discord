const ottoPog = "<:ottopog:837751302036783154>"
const tyhjiokass = "<:tyhjiokass:1108887711655411813>"

const roll = (msg: string): string => {
    const msgComponents = msg.split(" ").splice(1);
    const diceResult: number[] = diceRoll(msgComponents[0]);
    const diceSum = diceResult.reduce((previous, current) => previous + current, 0);
    const restOfArray = msgComponents.slice(1);
    const finalResult = calculateRest(diceSum, restOfArray);
    if (msgComponents.length == 1) {
        if (diceResult.length == 1 && diceResult[0] == 1) {
            return `${tyhjiokass} Juu thruu shit **${finalResult}!** ${tyhjiokass}`
        } else if (diceResult.length == 1 && diceResult[0] == 20) {
            return `${ottoPog} **Se on natural ${diceResult[0]}! ${ottoPog}**`;
        } else if (diceResult.length != 1) {
            return `Noppien tulos on **${finalResult}**! Sinä heitit **${diceResult.join(", ")}!**`
        } else {
            return `Nopanheittosi tulos on **${finalResult}**!`;
        }
    } else {
        if (diceResult[0] == 20) {
            return `${ottoPog} **Se on natural ${diceResult[0]}!** ${ottoPog}, mutta yhdistetty tulos on **${finalResult}**!`
        } else if (diceResult[0] == 1) {
            return `${tyhjiokass} Juu thruu shit **${diceResult[0]}!** ${tyhjiokass}, mutta yhdistetty tulos on **${finalResult}**!`
        } else {
            return `Kokonaistulos on **${finalResult}**! Sinä heitit **${diceResult.join(", ")}!**`
        }
    }
}

const diceRoll = (dice: string): number[] => {
    let diceComponents = dice.split("d");
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