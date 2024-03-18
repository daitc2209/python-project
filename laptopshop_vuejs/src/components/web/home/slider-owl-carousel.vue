<template>
  <div class="slider-owl-carousel owl-carousel">
		<div class="slider-item">
			<div class="content">
				<h3>Khuyến mãi lớn <br> <span>Lên tới 50%</span></h3>
				<p>Đắm chìm trong khả năng điện toán liền mạch với nhiều loại máy tính xách tay mạnh mẽ và kiểu dáng đẹp của Asus, được thiết kế cho người dùng hiện đại.</p>
				<a href="/store"><button id="shopnow">Mua ngay</button></a>
			</div>
			<div class="img"><img src="../../../images/slide/ASUS-1.png" alt=""></div>
		</div>
		<div class="slider-item">
			<div class="content">
				<h3>Khuyến mãi lớn <br> <span>Lên tới 70%</span></h3>
				<p>Trải nghiệm năng suất liền mạch và tay nghề xuất sắc với máy tính xách tay cao cấp của Dell, được thiết kế để hỗ trợ công việc của bạn.</p>
				<a href="/store"><button id="shopnow">Mua ngay</button></a>
			</div>
			<div class="img"><img src="../../../images/slide/DELL-1.png" alt=""></div>
		</div>
		<div class="slider-item">
			<div class="content">
				<h3>Khuyến mãi lớn <br> <span>Lên tới 60%</span></h3>
				<p>Trải nghiệm sự kết hợp hoàn hảo giữa hiệu suất và sự sang trọng với máy tính xách tay HP, được thiết kế để tăng năng suất của bạn.</p>
				<a href="/store"><button id="shopnow">Mua ngay</button></a>
			</div>
			<div class="img"><img src="../../../images/slide/HP-1.png" alt=""></div>
		</div>
	</div>
</template>

<script>

export default{
	mounted(){
		$(".slider-owl-carousel").owlCarousel({
			loop: true,
			margin: 10,
			nav: true,
			items: 1,
			dots: false,
			animateOut: 'fadeOut',
			animateIn: 'fadeIn',
			navText: ['<i class="fa fa-angle-left"></i>', '<i class="fa fa-angle-right"></i>'],
			smartSpeed: 2000,
			autoHeight: false,
			autoplay: true,
		});
	}
}
</script>

<style scoped>

</style>
