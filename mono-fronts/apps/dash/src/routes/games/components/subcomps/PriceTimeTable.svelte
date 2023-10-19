<script lang="ts">
    import { page } from "$app/stores";
    import type { Price, TimeTable } from "$lib/types";
    import { prices } from "$lib/stores";

    export let days: string[] = [];
    export let priceNumber: number = 0;
    export let timetable: TimeTable[] = [];
    export let refreshNumber: boolean = false;
    // prices: Price[] = [];

    const traduction = $page.data.user.traduction;
    let inputs: number[];
    let leftOver: number[];
    let tempVal: number = 0;
    if (timetable.length > 0) {
        inputs = timetable;
        tempVal = priceNumber;
        leftOver = timetable.reduce((newObj: number[], jose: number) => {
            tempVal = tempVal - jose;
            newObj.push(tempVal);
            return newObj;
        }, []);
    } else {
        inputs = new Array(days.length).fill(0);
        leftOver = new Array(days.length).fill(priceNumber);
    }

    $: if (refreshNumber) {
        tempVal = priceNumber;
        for (let i = 0; i < inputs.length; i++) {
            tempVal = tempVal - inputs[i];
            leftOver[i] = tempVal;
        }
        refreshNumber = false;
    }
    const upgraValues = (i: number) => {
        tempVal = priceNumber;
        for (let i = 0; i < inputs.length; i++) {
            tempVal = tempVal - inputs[i];
            leftOver[i] = tempVal;
        }
        // prices.update((prices) => {
        //     prices[priceNumber].timetable = { days, number: inputs };
        //     return prices;
        // });
    };
</script>

<div class="flex flex-col pt-10">
    {traduction.timetable_title}
    <div class="overflow-x-auto sm:-mx-6 lg:-mx-8">
        <div class="py-2 inline-block min-w-full sm:px-4 lg:px-8">
            <div class="overflow-hidden">
                <table class="min-w-full">
                    <thead class="bg-white border-b">
                        <tr>
                            <th
                                scope="col"
                                class="text-sm font-medium text-gray-900 px-4 py-4 text-left"
                            >
                                #
                            </th>
                            {#each days as day}
                                <th
                                    scope="col"
                                    class="text-sm font-medium text-gray-900 px-4 py-4 text-left"
                                >
                                    {day}
                                </th>
                            {/each}
                        </tr>
                    </thead>
                    <tbody>
                        <tr class="bg-white border-b">
                            <td
                                class="px-4 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
                            >
                                {traduction.timetable_entred}
                            </td>
                            {#each days as day, i}
                                <th
                                    scope="col"
                                    class="text-sm font-medium text-gray-900 px-4 py-4 text-left"
                                >
                                    <input
                                        type="text"
                                        name="winnableTimeRage-{i}"
                                        bind:value={inputs[i]}
                                        on:change={() => {
                                            upgraValues(i);
                                        }}
                                    />
                                </th>
                            {/each}
                        </tr>
                        <tr class="bg-gray-100 border-b">
                            <td
                                class="px-4 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
                            >
                                {traduction.timetable_left}
                            </td>
                            {#each days as day, i}
                                <th
                                    scope="col"
                                    class="text-sm font-medium text-gray-900 px-4 py-4 text-left"
                                >
                                    {leftOver[i]}
                                </th>
                            {/each}
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
