<script lang="ts">
    import { applyAction, enhance } from "$app/forms";
    import { goto, invalidateAll } from "$app/navigation";

    import type { ActionData } from "./$types";
    import type { PageData } from "./$types";
    import { page } from "$app/stores";

    export let form: ActionData;

    // export let data: PageData;
    const traduction = $page.data.user.traduction;
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
        <h3 class="text-2xl font-bold text-center">
            {traduction.recover_password}
        </h3>
        {#if form?.user}
            <p class="text-xs text-red-400 ml-3">
                {traduction.email_not_found}
            </p>
        {/if}
        <form
            method="post"
            action="?/forgot"
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
            <div class="mt-4">
                <div class="mt-4">
                    <label class="block" for="email"
                        >{traduction.email_tip}</label
                    >
                    <input
                        name="email"
                        type="email"
                        placeholder="Email"
                        required
                        class="w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-600"
                    />
                </div>
                <button
                    type="submit"
                    {disabled}
                    class=" py-2 text-white bg-{submitColor} rounded-lg px-10 flex my-4 shadow-lg shadow-{submitColor} font-bold {cursor} items-center justify-center text-center mx-auto"
                    >{@html submitText}</button
                >
            </div>
        </form>
    </div>
</div>
