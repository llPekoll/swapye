<script>
    export let title = "";
    export let subtitle = "";
    export let email = "";
    export let loggedAs = "";
</script>

<section class="w-full h-24 bg-white shadow-md md:ml-20 pt-2">
    <div class="float-right pr-2 md:pr-32  pt-3">
        <span class="text-sm float-right mt-2 -mb-2">{loggedAs}</span>
        <div class="font-thin">
            {email}
        </div>
    </div>

    <div class=" pl-6 md:pl-32 hidden md:block">
        <h1 class=" pt-3 text-2xl font-bold swapye-gray-dark capitalize  ">
            {title}
        </h1>
        <p class=" -mt-2 text-xl font-light swapye-gray-bright capitalize ">
            {subtitle}
        </p>
    </div>
</section>
