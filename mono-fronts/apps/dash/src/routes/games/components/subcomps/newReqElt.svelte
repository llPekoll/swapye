<script lang="ts">
    import {
        Listbox,
        ListboxButton,
        ListboxOptions,
        ListboxOption,
    } from "@rgossiaux/svelte-headlessui";
    import { CheckIcon, XCircleIcon } from "@rgossiaux/svelte-heroicons/solid";
    import Input from "$lib/components/Input.svelte";
    import { emblem } from "$lib/stores";
    import type { extraReqWordings } from "$lib/types";
    import { page } from "$app/stores";
    const traduction = $page.data.user.traduction;

    export let extraLangs: extraReqWordings[];
    export let needsUpdate = false;
    export let i: number = 0;
    export let elt = {
        kind: "input",
        key: "",
        id: 0,
        wordings: [
            {
                value: "",
                lang: "",
            },
        ],
    };
    console.log("elts", elt);
    let wordings: extraReqWordings[];
    let key = elt.key;
    console.log("key", key);
    let id = elt.id;
    if (elt.id !== 0) {
        wordings = elt.wordings;
    } else {
        wordings = extraLangs;
    }
    console.log("wordings", wordings);

    const instance = i;
    const people = [
        { id: 1, name: "Input" },
        { id: 2, name: "Checkbox" },
    ];

    let selectedPerson = people[1];
    if (elt.kind == "Input") {
        selectedPerson = people[0];
    } else if (elt.kind == "Checkbox") {
        selectedPerson = people[1];
    }
    let showMe = true;
    const deleteItem = async () => {
        if (!confirm(traduction.extra_delete_elt)) {
            return;
        }

        const urlToDel = `/perso/${$emblem}/extrarequesteds/${id}`;
        showMe = false;
        console.log("deleteItem", key);
        if (id !== 0) {
            await fetch(urlToDel, {
                method: "DELETE",
            });
        }
    };
</script>

{#if showMe}
    <input type="hidden" name="{instance}-key-id-{id}" value={id} />
    <input type="hidden" name="{instance}-option" value={selectedPerson.name} />
    <XCircleIcon
        class="h-7 w-7 text-red-500 cursor-pointer float-right"
        data-test="delete"
        on:click={deleteItem}
    />
    <span class="text-4xl text-slate-400">.{i + 1}</span>
    <div class="ml-3">
        <!-- <input type="text" name={key} /> -->

        <span class="float-left mt-4">{traduction.extra_req_type}</span>
        <Listbox
            value={selectedPerson}
            on:change={(e) => (
                (selectedPerson = e.detail), (needsUpdate = true)
            )}
            class="relative w-1/3"
        >
            <ListboxButton
                class="relative w-full py-2 pl-3 pr-10 text-left bg-white rounded-lg shadow-md cursor-default focus:outline-none focus-visible:ring-2 focus-visible:ring-opacity-75 focus-visible:ring-white focus-visible:ring-offset-orange-300 focus-visible:ring-offset-2 focus-visible:border-indigo-500 sm:text-sm"
            >
                {selectedPerson.name}
                <span
                    class="absolute inset-y-0 right-0 flex items-center pr-2 pointer-events-none"
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 20 20"
                        fill="currentColor"
                        aria-hidden="true"
                        class="w-5 h-5 text-gray-400"
                        ><path
                            fill-rule="evenodd"
                            d="M10 3a1 1 0 01.707.293l3 3a1 1 0 01-1.414 1.414L10 5.414 7.707 7.707a1 1 0 01-1.414-1.414l3-3A1 1 0 0110 3zm-3.707 9.293a1 1 0 011.414 0L10 14.586l2.293-2.293a1 1 0 011.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z"
                            clip-rule="evenodd"
                        /></svg
                    >
                </span>
            </ListboxButton>
            <ListboxOptions
                class="absolute w-full py-1 mt-1 overflow-auto text-base bg-white rounded-md shadow-lg max-h-60 ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm"
            >
                {#each people as person (person.id)}
                    <ListboxOption
                        value={person}
                        let:selected
                        class={({ active }) => (active ? "sakommd" : "papou")}
                    >
                        {#if selected}
                            <span class="absolute left-3">
                                <CheckIcon class="w-5 " />
                            </span>
                        {/if}
                        {person.name}
                    </ListboxOption>
                {/each}
            </ListboxOptions>
        </Listbox>

        <Input
            name={traduction.extra_req_key}
            val={key}
            inputName="{instance}-key"
            bind:needsUpdate
        />
        <div class="ml-5">
            {#each wordings as { lang, wording }, i}
                <div>
                    <p>{traduction.extra_req_val} {lang.split(" ")[0]}</p>
                    <div class="md:w-2/3 ml-4">
                        <input
                            type="text"
                            name="{instance}-key-{lang}"
                            class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-blue-500"
                            value={wording ? wording : ""}
                            on:blur={() => (needsUpdate = true)}
                        />
                    </div>
                </div>
            {/each}
        </div>
    </div>
{/if}

<style>
    /* WARNING: This is just for demonstration.
      Using :global() in this way can be risky. */
    :global(.sakommd) {
        @apply cursor-default select-none relative py-2 pl-10 pr-4 text-gray-900 bg-yellow-300;
    }

    :global(.papou) {
        @apply cursor-default select-none relative py-2 pl-10 pr-4 text-gray-900;
    }
</style>
