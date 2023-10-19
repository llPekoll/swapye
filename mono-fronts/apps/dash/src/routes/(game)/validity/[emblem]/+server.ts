import { env } from "$lib/env.js";
import type { RequestHandler } from "../$types";
import { json } from "@sveltejs/kit";

export const GET: RequestHandler = async ({ params, locals }) => {
    const url = `${env.VITE_BACKEND_DNS}/game/validator/${params.emblem}`;
    const res = await fetch(url, {
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
        },
    });
    return json(await res.json());
};
