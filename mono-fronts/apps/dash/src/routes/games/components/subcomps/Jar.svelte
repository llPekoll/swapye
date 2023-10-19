<script lang="ts">
    import {
        RadioGroup,
        RadioGroupLabel,
        RadioGroupOption,
    } from "@rgossiaux/svelte-headlessui";
    import type { GameType, Skin } from "$lib/types";
    export let listOf: GameType[] | Skin[];
    export let title = "";
    export let id = 0;
    export let updateFunction: (e: number) => void;
</script>

<div class="">
    <RadioGroup value={id} on:change={(e) => updateFunction(e.detail)}>
        <RadioGroupLabel>{title}:</RadioGroupLabel>
        {#each listOf as { name, ref_id }}
            <RadioGroupOption
                value={ref_id}
                let:checked
                class="bg-slate-100 relative rounded-lg shadow-md cursor-pointer flex focus:outline-none h-10 items-center my-1"
            >
                <span class:checked>
                    <p class="pl-10">
                        {name}
                    </p>
                    {#if checked}
                        <div class="text-white absolute right-5">
                            <svg
                                viewBox="0 0 24 24"
                                fill="none"
                                class="w-6 h-6"
                            >
                                <circle
                                    cx="12"
                                    cy="12"
                                    r="12"
                                    fill="#fff"
                                    opacity="0.2"
                                />
                                <path
                                    d="M7 13l3 3 7-7"
                                    stroke="#fff"
                                    stroke-width="1.5"
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                />
                            </svg>
                        </div>
                    {/if}
                </span>
            </RadioGroupOption>
        {/each}
    </RadioGroup>
</div>
