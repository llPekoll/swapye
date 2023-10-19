<script lang="ts">
    import type { ActionData, PageData } from "./$types";
    import { invalidateAll } from "$app/navigation";
    import { applyAction, enhance } from "$app/forms";

    export let form: ActionData;
    export let data: PageData;
    console.log(data);
    console.log(data.trads);
    const traduction = data.trads;

    let cursor = "cursor-pointer";
    let submitText = traduction.submit;
    let submitColor = "bleu-gris";
    let disabled = false;
</script>

<div class="flex items-center justify-center min-h-screen bg-gray-100">
    <div
        class="px-8 py-6 mx-4 mt-4 text-left bg-white shadow-lg md:w-4/5 lg:w-1/2 w-full"
    >
        <div class="flex justify-center">
            <img src={traduction.logo_swapye_couleur} alt="logo" class="w-14" />
        </div>
        <h3 class="text-2xl font-bold text-center">{traduction.login}</h3>
        {#if form?.invalid}
            <p
                class="bg-red-100 text-red-500 rounded mx-auto text-center py-2 w-1/2 my-2 italic border-red-400 border"
            >
                {traduction.email_pass_not_match}
            </p>
        {/if}
        <form
            method="POST"
            action="?/login"
            use:enhance={({ form }) => {
                submitText = `<svg width="3em" height="3em" viewBox="0 0 24 24"><circle cx="18" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin=".67" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle><circle cx="12" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin=".33" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle><circle cx="6" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin="0" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle></svg>`;
                submitColor = "bleu-gris/[.3]";
                cursor = "cursor-not-allowed";
                disabled = true;

                return async ({ result, update }) => {
                    console.log("result");
                    console.log(result);
                    // @ts-ignore
                    if (result.data?.invalid) {
                        cursor = "cursor-pointer";
                        submitText = traduction.submit;
                        submitColor = "bleu-gris";
                        disabled = false;
                        return;
                    }
                    await applyAction(result);
                    await invalidateAll();
                };
            }}
        >
            <div class="my-10">
                <div class="mt-4">
                    <label class="block form__label" for="email"
                        >{traduction.email_tip}</label
                    >
                    <input
                        type="text"
                        placeholder="Email"
                        name="email"
                        data-test="email-log"
                        class="form__field w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-600"
                    />
                </div>
                <div class="mt-4">
                    <label class="block form__label" for="password"
                        >{traduction.password}</label
                    >
                    <input
                        data-test="password"
                        type="password"
                        placeholder="Password"
                        name="password"
                        class="form__field w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-1 focus:ring-blue-600"
                        required
                    />
                </div>
                <button
                    data-test="submit"
                    type="submit"
                    {disabled}
                    class=" py-2 text-white bg-{submitColor} rounded-lg w-1/3 flex my-4 shadow-lg shadow-{submitColor} font-bold {cursor} items-center justify-center text-center mx-auto"
                    >{@html submitText}</button
                >
                <p class="pt-2">
                    <a href="/forgot" class="text-blue-600 underline text-sm">
                        {traduction.reset_password}
                    </a>
                </p>
                <div class="mt-6 text-grey-dark text-center">
                    {traduction.no_account}
                    <a class="text-blue-600 hover:underline" href="/register">
                        {traduction.register}
                    </a>
                </div>
            </div>
        </form>
    </div>
</div>
