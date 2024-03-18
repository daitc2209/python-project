<template>
  <footer class="main-footer text-center">
		<strong>Copyright &copy; <strong>{{ getCurrentYear }}</strong> 
			<a href="/home">TCD</a>.
		</strong> All rights reserved.
	</footer>
</template>

<script>
export default {
	computed: {
    getCurrentYear() {
      return new Date().getFullYear();
    }
  }
}
</script>

<style>

</style>