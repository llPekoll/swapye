/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./src/**/*.{html,js,svelte,ts}"],
    theme: {
        extend: {
            colors: {
                "vert-menthe": "#82C6A6",
                "bleu-gris": "#3D516D",
                "bleu-swapye-1": "#5C58FF",
                "bleu-swapye-2": "#817EFF",
                "bleu-swapye-3": "#CIBFFF",
                "gris-sombre": "#1B1B1B",
                "gris-clair": "#F3F3F3",
                "gris-moyen": "#4D4D4D",
                "new-orange": "#FA9131",
                "dash-grey": "#F9F9FA",
            },
        },
    },
    plugins: [],
};
