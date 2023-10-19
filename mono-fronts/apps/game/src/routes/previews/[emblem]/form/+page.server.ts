import { env } from "$lib/env.js";
import { error } from '@sveltejs/kit';

export const load = async ({ params }) => {
    const res4 = await fetch(
        `${env.VITE_BACKEND_DNS}/game/validator/${params.emblem}`
    );
    const validator = await res4.json();
    console.log({ validator });
    if (validator.errors.length > 0) {
        throw error(500, {
            message: validator.errors.join('<br/>')
        });

    }
    const [tradsRes, langsRes] = await Promise.all([

        fetch(`${env.VITE_BACKEND_DNS}/game/trads/${params.emblem}`),
        fetch(`${env.VITE_BACKEND_DNS}/game/langs/${params.emblem}`)
    ]);

    const [trads, langs] = await Promise.all([
        tradsRes.json(),
        langsRes.json()
    ])
    return {
        trads,
        langs,
    };
};