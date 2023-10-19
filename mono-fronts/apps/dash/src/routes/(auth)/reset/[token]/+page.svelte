<script lang="ts">
    import type { PageData } from "./$types";
    import { goto } from "$app/navigation";
    import { applyAction, enhance } from "$app/forms";
    import { invalidateAll } from "$app/navigation";
    import { page } from "$app/stores";
    export let data: PageData;
    const traduction = $page.data.user.traduction;
    let password = "";
    let password_confirm = "";

    let longerPass = false;
    let samePassword = false;
    let canSubmit = false;

    $: if (password.length > 1) {
        samePassword = password_confirm == password;
    }
    $: if (password.length > 3) {
        longerPass = true;
    } else {
        longerPass = false;
    }

    $: if (samePassword && longerPass) {
        canSubmit = true;
    }

    let cursor = "cursor-pointer";
    let submitText = traduction.submit;
    let submitColor = "bleu-gris";
    let disabled = false;
</script>

<div class="flex items-center justify-center min-h-screen bg-gray-100">
    <div
        class="px-8 py-6 mx-4 mt-4 text-left bg-white shadow-lg md:w-1/3 lg:w-1/3 sm:w-1/3"
    >
        <div class="flex justify-center">
            <img src={traduction.logo_swapye_couleur} alt="logo" class="w-14" />
        </div>
        <h3 class="text-2xl font-bold text-center">{traduction.restes_pass}</h3>
        <form
            method="POST"
            action="?/reset"
            use:enhance={({ form }) => {
                submitText = `<svg width="3em" height="3em" viewBox="0 0 24 24"><circle cx="18" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin=".67" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle><circle cx="12" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin=".33" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle><circle cx="6" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin="0" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle></svg>`;
                submitColor = "bleu-gris/[.3]";
                cursor = "cursor-not-allowed";
                disabled = true;
                return async ({ result, update }) => {
                    await applyAction(result);
                    await invalidateAll();
                    goto("/login");
                };
            }}
        >
            <input type="hidden" name="token" value={data.token} />
            <div class="mt-4">
                <div class="mt-4">
                    <label class="block" for="password"
                        >{traduction.password}</label
                    >
                    <input
                        bind:value={password}
                        name="password"
                        type="password"
                        placeholder="Password"
                        class="w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-600"
                    />
                </div>
                <div class="mt-4">
                    <label class="block" for="password_confirm"
                        >{traduction.confirm_password}</label
                    >
                    <input
                        bind:value={password_confirm}
                        id="password_confirm"
                        type="password"
                        placeholder="Password"
                        class="w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-600"
                    />
                </div>
                {#if !samePassword}
                    <p class="text-xs text-red-400 ml-3">
                        • {traduction.same_password}
                    </p>
                {/if}
                {#if !longerPass}
                    <p class="text-xs text-red-400 ml-3">
                        • {traduction.four_char_min}
                    </p>
                {/if}
                {#if canSubmit}
                    <button
                        data-test="submit"
                        type="submit"
                        {disabled}
                        class=" py-2 text-white bg-{submitColor} rounded-lg w-1/3 flex my-4 shadow-lg shadow-{submitColor} font-bold {cursor} items-center justify-center text-center mx-auto"
                        >{@html submitText}</button
                    >
                {:else}
                    <button
                        type="submit"
                        disabled
                        class="w-full px-6 py-2 mt-4 text-white bg-slate-300 rounded-lg"
                        >{traduction.account_creation}</button
                    >
                {/if}
            </div>
        </form>
    </div>
</div>
