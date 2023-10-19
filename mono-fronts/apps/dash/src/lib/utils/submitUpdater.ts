export const submitUpdater = (
    needsUpdate: boolean,
    submitColor: string,
    cursor: string,
    disabled: boolean
): void => {
    if (needsUpdate) {
        submitColor = "bleu-gris";
        cursor = "cursor-pointer";
        disabled = false;
    } else {
        submitColor = "bleu-gris/[.3]";
        cursor = "cursor-not-allowed";
        disabled = true;
    }
    return;
}