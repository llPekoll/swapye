const areSame = (currentValue: number, _: number, array: number[]) =>
    currentValue === array[0];

const onlyUnique = (value: number, index: number, self: number[]) => {
    return self.indexOf(value) === index;
};

const doublePosition = (item: number, arr: number[]) => {
    const index = arr.indexOf(item);
    if (index === 0) {
        return Math.floor(Math.random() * 2) + 1;
    }
    if (index === 1) {
        return Math.floor(Math.random() * 2) > 0 ? 2 : 0;
    } else {
        return Math.floor(Math.random() * 2);
    }
};

export const gameResult = (arr: number[]) => {
    const localArr = arr.filter(onlyUnique);
    if (!localArr || !Array.isArray(localArr)) {
        throw new Error("Function expect an array as parameter");
    }
    if (localArr.length < 3) {
        throw new Error("Array should have at least 3 values");
    }
    if (localArr.every(areSame)) {
        throw new Error("Array values shouldn't be the same");
    }
    const shuffledArray = localArr.sort((a, b) => 0.5 - Math.random());
    let newArr = shuffledArray.slice(0, 3);
    const isDouble = Math.ceil(Math.random() * 10) > 5 ? true : false;
    const whoIsDouble = localArr[Math.floor(Math.random() * 3)];
    const position = doublePosition(whoIsDouble, localArr);
    if (isDouble) {
        newArr[position] = whoIsDouble;
    }
    return newArr;
};
