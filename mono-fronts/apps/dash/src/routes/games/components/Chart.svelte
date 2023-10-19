<script lang="ts">
    import { Doughnut } from "svelte-chartjs";

    import {
        Chart as ChartJS,
        Title,
        Tooltip,
        Legend,
        ArcElement,
        CategoryScale,
    } from "chart.js";
    import { page } from "$app/stores";

    export let left: number = 0;
    export let total: number = 0;
    const traduction = $page.data.user.traduction;
    const data = {
        labels: [traduction.chart_price_won, traduction.chart_price_let],
        datasets: [
            {
                data: [left, total - left],
                backgroundColor: [
                    "#F7464A",
                    "#46BFBD",
                    "#FDB45C",
                    "#949FB1",
                    "#4D5360",
                    "#AC64AD",
                ],
                hoverBackgroundColor: [
                    "#FF5A5E",
                    "#5AD3D1",
                    "#FFC870",
                    "#A8B3C5",
                    "#616774",
                    "#DA92DB",
                ],
            },
        ],
    };

    ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale);
</script>

<Doughnut
    {data}
    options={{ maintainAspectRatio: false }}
    width={500}
    height={300}
/>
