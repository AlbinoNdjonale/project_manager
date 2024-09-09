<script setup>
   import ProjectView from "../views/ProjectView.vue";

   const props = defineProps({
      link: {
         required: true,
         type: String
      }
   })
</script>
   
<template>
   <ProjectView :invite = 'true' :link = 'link'/>
</template>