<script lang="ts">
    import { json } from "@sveltejs/kit";
    import { stringify } from "postcss";
    import { formSubmited } from "$lib/stores";

    type Type = "image" | "text";
    interface Price {
        id: number;
        type: Type;
        value: "string";
        tradPacks: {
            value: string;
            lang: string;
        };
    }
    export let price: Price = {};
    export let className = "";
    export let style = "";
    export let prices: Price[] = [];
    export let winnerReelsPrice = false;

    console.log("price");
    console.log(price);
    let newPriceList = Array(19).fill(prices).flat();
    newPriceList = newPriceList.slice(0, 19 * 3);
    newPriceList = newPriceList.sort((a, b) => 0.5 - Math.random());
    $: if ($formSubmited) {
        style = `margin-top: 0; transition-duration: 0ms;`;
    }
    $: if (winnerReelsPrice) {
        newPriceList = Array(19).fill(prices).flat();
        newPriceList = newPriceList.slice(0, 19 * 3);
        newPriceList = newPriceList.sort((a, b) => 0.5 - Math.random());
        console.log("The price");
        console.log(price);
        // newPriceList = [...newPriceList, price];
        console.log("newPriceList ======== 1");
        console.log(newPriceList);
        newPriceList.push(price);
        console.log("newPriceList ======== 2");
        console.log("newPriceList");
        console.log(newPriceList);
        newPriceList = newPriceList.filter(function (element) {
            return element !== undefined;
        });
        newPriceList = newPriceList.map((price) => {
            // console.log("price");
            // console.log(price);
            return {
                type: price.img ? "img" : "text",
                value: price.img ? price.img : price.name,
            };
        });
        console.log("newPriceList  ======== 3");
        console.log(newPriceList);
    }
</script>

<div class={className} {style}>
    {#each newPriceList as { type, value }}
        {#if type === "img"}
            <img
                src={value}
                alt="cadeaux Slot machine"
                style="border: 1px solid black;"
            />
        {:else}
            <div>
                <p>{value}</p>
            </div>
        {/if}
    {/each}
</div>

<style>
    .reel {
        background-repeat: repeat-y;
        z-index: 2;
        position: absolute;
        top: 0;
        left: 76px;
        height: 8000px;
        width: 140px;
        background-position: 0 0;
        transition: margin-top 5s ease-out;
        margin-top: 0px;
    }
    .reel-left {
        left: 0;
    }
    .reel-right {
        left: auto;
        right: 0;
    }
    .reel-center {
        left: 0;
        right: 0;
        margin: 0 auto;
    }
    .reel-left {
        left: 0;
    }
    .reel-right {
        left: auto;
        right: 0;
    }
    .reel-center {
        left: 0;
        right: 0;
        margin: 0 auto;
        width: 156px;
    }
    * {
        box-sizing: border-box;
    }
    .reel > img,
    .reel > div {
        width: 100%;
        height: 142px;
    }
    .reel > div {
        display: flex;
        align-items: center;
        justify-content: center; /* optional */
        background: #eee; /* optional */
    }
    .reel > div > p {
        font-weight: 600;
        padding: 0 10px;
    }
    @media screen and (max-width: 1279px) {
        .reel {
            width: 111px;
        }
        .reel > img,
        .reel > div {
            height: 111px;
        }
    }
    @media (max-width: 600px) {
        .reel {
            width: 65px;
            font-size: 0.7rem;
            line-height: 1.2;
        }
        .reel-center {
            width: 71px;
        }
        .reel > img,
        .reel > div {
            height: 67px;
        }
    }
</style>
