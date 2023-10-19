import { env } from "$lib/env.js";
import { error } from '@sveltejs/kit';
import type { Action, Actions, PageServerLoad } from "./$types";
import { fail, redirect } from "@sveltejs/kit";


export const load: PageServerLoad = async ({ params }) => {
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
    const [tradsRes, gameRes, pricesRes, langsRes] = await Promise.all([

        fetch(`${env.VITE_BACKEND_DNS}/game/trads/${params.emblem}`),
        fetch(`${env.VITE_BACKEND_DNS}/game/${params.emblem}`),
        fetch(`${env.VITE_BACKEND_DNS}/dash/${params.emblem}/prices/game`),
        fetch(`${env.VITE_BACKEND_DNS}/game/langs/${params.emblem}`)
    ]);

    const [trads, game, prices, langs] = await Promise.all([
        tradsRes.json(),
        gameRes.json(),
        pricesRes.json(),
        langsRes.json()
    ])
    const now = new Date(Date.now());
    const start = new Date(game.startDate);
    const end = new Date(game.endDate);
    if (!game.unlimitedInTime) {
        if (now < start) {
            throw redirect(302, "/notyet");
        }
        if (now > end) {
            throw redirect(302, "/over");
        }
    }
    return {
        trads,
        game,
        prices,
        langs,
    };
};




const postgameform: Action = async ({ request, locals }) => {
    console.log("==== Edit Identity =====");
    const data: FormData = await request.formData();

    var payload = {};
    data.forEach(function (value, key) {
        payload[key] = value;
    });

    console.log("payload");
    console.log(payload);
    try {
        const res = await fetch(
            `${env.VITE_BACKEND_DNS}/leads`,
            {
                headers: {
                    Accept: "application/json",
                    "Content-Type": "application/json",
                },
                method: "POST",
                body: JSON.stringify(payload),
            }
        );
        return await res.json();
    } catch {
        return fail(400, { edit: true });
    }
};

export const actions: Actions = { postgameform };
