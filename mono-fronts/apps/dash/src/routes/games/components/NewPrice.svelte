<script lang="ts">
    import type { Price } from "$lib/types";
    import { toast } from "@zerodevx/svelte-toast";
    import { emblem, prices, dateNregion } from "$lib/stores";
    import { RefreshIcon } from "@rgossiaux/svelte-heroicons/solid";

    import { page } from "$app/stores";
    import { enhance } from "$app/forms";
    import CheckBox from "$lib/components/CheckBox.svelte";
    import TimeTable from "./subcomps/PriceTimeTable.svelte";
    import PriceImg from "./subcomps/PriceImg.svelte";
    import Loading from "$lib/components/Loading.svelte";
    import { errorToast, successToast } from "$lib/toastTheme";

    export let price: Price;
    export let days: string[] = [];
    export let langs: string[] = [];
    export let updaloed = false;
    export let isLoading = false;
    export let updateTitles = false;
    export let priceName = "New Price";
    const traduction = $page.data.user.traduction;
    const unlimitedInTime = $dateNregion.unlimitedInTime;
    let action = price.id ? `?/priceedit` : `?/pricecreate`;
    console.log("Price \n", price);

    let showMe = true;
    const deleteItem = async () => {
        if (!confirm("Etes vous sure de vouloir supprimer ce prix?")) {
            return;
        }
        const urlToDel = `${$page.url.href}`;
        showMe = false;
        if (price.id) {
            await fetch(urlToDel, {
                method: "DELETE",
                body: JSON.stringify({
                    id: price.id,
                    emblem: emblem,
                }),
            });
        }
        // Delete element from list prices
        var removeIndex = $prices.map((p) => p.id).indexOf(price.id);
        const newList = $prices.splice(removeIndex, 1);

        prices.set(newList);
    };

    let refreshNumber = false;
    const updatePrices = () => {
        refreshNumber = true;
    };
    let star = `${traduction.price_consolation_price}**`;
    let inRotation = false;
    const reload = async () => {
        const url = `/perso/${$emblem}/price/${price.id}`;
        inRotation = true;
        const res = await fetch(url);
        const data = await res.json();
        langs = data.price.trads;
        price.id = data.price.id;
        price.name = data.price.name;
        price.number = data.price.number;
        price.img = data.price.img;
        price.emailTemplate = data.price.emailTemplate;
        price.consolationPrice = data.price.consolationPrice;
        price.displayPriceName = data.price.displayPriceName;
        price.timetable = data.timetable;
        inRotation = false;
    };

    let submitText = traduction.submit;
    let submitColor = "bleu-gris";
    let cursor = "cursor-pointer";

    let needsUpdate = false;
    let disabled = true;

    $: if (needsUpdate) {
        submitText = traduction.submit;
        submitColor = "bleu-gris";
        cursor = "cursor-pointer";
        disabled = false;
    } else {
        submitText = traduction.submit;
        submitColor = "bleu-gris/[.3]";
        cursor = "cursor-not-allowed";
        disabled = true;
    }
    const updateTitle = (e: HTMLInputElement, lang: string) => {
        if (price.tradPacks[0].lang == lang) {
            priceName = e.target.value;
            updateTitles = true;
        }
    };
</script>

{#if showMe}
    <div>
        <form
            class="bg-slate-100 rounded shadow"
            enctype="multipart/form-data"
            method="POST"
            {action}
            use:enhance={({ form }) => {
                submitText = `<svg width="3em" height="3em" viewBox="0 0 24 24"><circle cx="18" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin=".67" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle><circle cx="12" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin=".33" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle><circle cx="6" cy="12" r="0" fill="currentColor"><animate attributeName="r" begin="0" calcMode="spline" dur="1.5s" keySplines="0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8;0.2 0.2 0.4 0.8" repeatCount="indefinite" values="0;2;0;0"></animate></circle></svg>`;
                submitColor = "bleu-gris/[.3]";
                cursor = "cursor-not-allowed";
                return async ({ result }) => {
                    console.log(1);

                    if (result.type === "success") {
                        console.log("result.data");
                        console.log(result.data);
                        price.id = result.data?.id;
                        price.name = result.data?.name;
                        price.number = result.data?.number;
                        price.img = result.data?.img;
                        price.emailTemplate = result.data?.emailTemplate;
                        price.consolationPrice = result.data?.consolationPrice;
                        price.displayPriceName = result.data?.displayPriceName;
                        price.timetable = result.data?.timetable;
                        price.tradPacks = result.data?.tradPacks;
                        // update this price from the store
                        console.log("price.tradPacks");
                        console.log(price.tradPacks);
                        if (action !== `?/priceedit`) {
                            console.log(4);
                            price.id = result.data?.id;
                            price.name = result.data?.name;
                            price.number = result.data?.number;
                            price.img = result.data?.img;
                            price.emailTemplate = result.data?.emailTemplate;
                            price.consolationPrice =
                                result.data?.consolationPrice;
                            price.displayPriceName =
                                result.data?.displayPriceName;
                            price.timetable = result.data?.timetable;
                            price.tradPacks = result.data?.tradPacks;

                            console.log(5);
                            const newPrice = {
                                id: result.data?.id,
                                name: result.data?.name,
                                number: result.data?.number,
                                img: result.data?.img,
                                emailTemplate: result.data?.emailTemplate,
                                consolationPrice: result.data?.consolationPrice,
                                displayPriceName: result.data?.displayPriceName,
                                timetable: result.data?.timetable,
                                tradPacks: result.data?.tradPacks,
                            };
                            console.log(6);
                            prices.set({
                                prices: [...$prices.prices, newPrice],
                                langs: langs,
                                days: days,
                            });
                        }
                        console.log(7);
                        console.log(price);

                        toast.push(traduction.toast_success, {
                            ...successToast,
                        });
                    } else {
                        toast.push(
                            `${traduction.toast_error}, ${result.error.message}`,
                            {
                                ...errorToast,
                            }
                        );
                    }
                    needsUpdate = false;
                    action = `?/priceedit`;
                };
            }}
        >
            <input type="hidden" name="emblem" value={$emblem} />
            {#if price.id}
                <input type="hidden" name="id" value={price.id} />
            {/if}
            <div class="rounded-lg mb-10 px-10 py-10">
                <div
                    on:click={deleteItem}
                    on:keyup={deleteItem}
                    class="py-4 float-right"
                >
                    <svg
                        class="fill-red-500"
                        width="2em"
                        height="2em"
                        viewBox="0 0 24 24"
                    >
                        <path
                            d="M12 3c-4.963 0-9 4.038-9 9s4.037 9 9 9s9-4.038 9-9s-4.037-9-9-9zm0 16c-3.859 0-7-3.14-7-7s3.141-7 7-7s7 3.14 7 7s-3.141 7-7 7zm.707-7l2.646-2.646a.502.502 0 0 0 0-.707a.502.502 0 0 0-.707 0L12 11.293L9.354 8.646a.5.5 0 0 0-.707.707L11.293 12l-2.646 2.646a.5.5 0 0 0 .707.708L12 12.707l2.646 2.646a.5.5 0 1 0 .708-.706L12.707 12z"
                        /></svg
                    >
                </div>
                <p class=" px-5 italic pt-3 pb-5 text-3xl text-slate-500">
                    <RefreshIcon
                        class="h-10 w-10 {inRotation
                            ? 'rotate-360 animate-spin'
                            : ''}"
                        on:click={reload}
                    />
                </p>

                {#each price.tradPacks as { lang, src }}
                    <PriceImg {src} {lang} {updaloed} />
                {/each}
                {#each price.tradPacks as { lang, name }}
                    <div class="inline">
                        <label for="endText" class="text-slate-600"
                            >{traduction.price_name_price}
                            <span class="text-xs">{lang} </span>
                            <div
                                on:click={() => (needsUpdate = true)}
                                on:keypress={() => (needsUpdate = true)}
                            >
                                <input
                                    on:keyup={(e) => {
                                        updateTitle(e, lang);
                                    }}
                                    type="text"
                                    name="name-{lang}"
                                    class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-blue-500"
                                    required
                                    value={name ? name : ""}
                                />
                            </div>
                        </label>
                    </div>
                {/each}
                <div class="group mt-10">
                    <label for="name" class="text-slate-600"
                        >{traduction.price_number_price}</label
                    >
                    <div
                        on:click={() => (needsUpdate = true)}
                        on:keypress={() => (needsUpdate = true)}
                    >
                        <input
                            type="number"
                            name="quantity"
                            class="bg-gray-200 appearance-none border-2 border-gray-200 rounded py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-blue-500 float-right"
                            required
                            bind:value={price.number}
                            on:blur={updatePrices}
                        />
                        <div class="bar" />
                    </div>
                </div>
                <div class="group mt-10">
                    <label for="name" class="text-slate-600"
                        >{traduction.template_email_price}*</label
                    >
                    <div
                        on:click={() => (needsUpdate = true)}
                        on:keypress={() => (needsUpdate = true)}
                    >
                        <input
                            type="text"
                            name="emailTemplate"
                            class="bg-gray-200 appearance-none border-2 border-gray-200 rounded py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-blue-500 float-right"
                            value={price.emailTemplate}
                        />
                        <div class="bar" />
                    </div>
                </div>
                <div class="mt-10" />
                <div
                    on:click={() => (needsUpdate = true)}
                    on:keypress={() => (needsUpdate = true)}
                >
                    <CheckBox
                        valueToSet={price.consolationPrice}
                        tradsToDisp={star}
                        name="consolationPrice"
                    />
                </div>
                <div
                    on:click={() => (needsUpdate = true)}
                    on:keypress={() => (needsUpdate = true)}
                >
                    <CheckBox
                        valueToSet={price.displayPriceName}
                        tradsToDisp={traduction.price_disp_price}
                        name="displayPriceName"
                    />
                </div>
                <div class="w-full">
                    {#if isLoading}
                        <Loading />
                    {:else if unlimitedInTime || days.length == 0}
                        {#if unlimitedInTime}
                            <p class="py-4 text-orange-500">
                                {traduction.no_time_table_for_unlimited_in_t}
                            </p>
                        {/if}
                        {#if days.length == 0 && !unlimitedInTime}
                            <p class="text-red-500">
                                {traduction.no_day_to_disp_time_table}
                            </p>
                        {/if}
                    {:else}
                        <div
                            on:click={() => (needsUpdate = true)}
                            on:keypress={() => (needsUpdate = true)}
                        >
                            <TimeTable
                                bind:days
                                bind:timetable={price.timetable}
                                bind:priceNumber={price.number}
                                bind:refreshNumber
                            />
                        </div>
                    {/if}
                </div>
                <button
                    type="submit"
                    class="px-10 py-2 text-white bg-{submitColor} rounded-lg mx-auto text-center w-1/3 flex my-4 shadow-lg shadow-{submitColor} font-bold {cursor}"
                    data-test="submit"
                    {disabled}
                >
                    <p class="mx-auto text-center">
                        {@html submitText}
                    </p>
                </button>
            </div>
        </form>
    </div>
{/if}
