<template>
  <footer id="footer">
	<div class="footer-top">
	 	<div class="footer-wrapper-1 py-2">
          <div class="container">
            <div class="row align-items-center">
              <div class="col-lg-4 my-3">
                <div class="footer-top-data d-flex gap-30 align-items-center">
                  <h2 class='mb-0 text-white'>Đăng ký nhận thông báo</h2>
                </div>
              </div>
              <div class="col-lg-8 my-3">
                <div class="input-group">
                  <input 
                  type="text"
                  class="form-control py-1"
                  placeholder="Your Email Address"
                  aria-label="Your Email Address"
                  aria-describedby="basic-addon2"
                  />
                  <span class="input-group-text py-2" id="basic-addon2">
                    Đăng ký
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
	</div>
	<hr>
  <div class="footer-container">
    <div class="container py-4 text-center">
      <span class="footer__heading">Địa chỉ cửa hàng</span>
      <ul class="footer-list">
        <li class="footer-item"><a href="#" class="footer-item__link">60-49 Road 11378 New York</a> </li>
        <li class="footer-item"><a href="#" class="footer-item__link">daitc2209@gmail.com </a></li>
        <li class="footer-item"><a href="#" class="footer-item__link">0906088493</a></li>
      </ul>
    </div>
    <div class="container py-4 text-center">
      <span class="footer__heading">Liên hệ</span>
      <ul class="footer-list">
        <li class="footer-item">
          <a href="#" class="footer-item__link">
              <i class="fab fa-facebook"></i>
              Facebook
          </a>
        </li>
        <li class="footer-item">
          <a href="#" class="footer-item__link">
              <i class="fab fa-instagram"></i>
              Instagram
          </a>
        </li>
        <li class="footer-item">
          <a href="#" class="footer-item__link">
              <i class="fa-brands fa-twitter"></i>
              Twitter
          </a>
        </li>
      </ul>
    </div>
    <div class="container py-4 text-center">
      <span class="footer__heading">Chính sách</span>
      <ul class="footer-list">
        <li class="footer-item"><a href="#" class="footer-item__link">Vận chuyển & Đổi trả</a> </li>
        <li class="footer-item"><a href="#" class="footer-item__link">Điều khoản & Điều kiện</a></li>
        <li class="footer-item"><a href="#" class="footer-item__link">Phương thức thanh toán </a></li>
        <li class="footer-item"><a href="#" class="footer-item__link">FAQ</a></li>
      </ul>
    </div>
    <div class="container py-4 text-center">
      <span class="footer__heading">Hỗ trợ</span>
      <ul class="footer-list">
        <li class="footer-item"><a href="/contact" class="footer-item__link">Liên hệ</a> </li>
        <li class="footer-item"><a href="/about" class="footer-item__link">Giới thiệu</a></li>
      </ul>
    </div>
  </div>
	<div class="container py-4 ">
		<div class="copyright">
			&copy; Copyright 
			<strong>{{ getCurrentYear }}</strong> 
			<strong>TCD</strong>. All Rights Reserved
		</div>
	</div>
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
.footer__heading{
  text-transform: uppercase;
  font-size: 24px;
  color: #fff;
}
.footer-list{
  list-style: none;
  margin-top: 12px;
}
.footer-item{
  padding: 2px 0;
  margin: 6px 0;
}
.footer-item__link{
  line-height: 24px;
  font-size: 16px;
  color: #fff;
  transition: color .3s ease;
}
.footer-container{
  display: flex;
  margin: 4px;
}
</style>