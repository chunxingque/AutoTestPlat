<template>
	<div class="home-container">
		<div class="home-content">
			<h1>自动化测试系统</h1>
			<p>欢迎使用自动化测试系统,此系统支持Web自动化测试,支持设置定时任务与定时任务管理等等,其他新功能努力开发中</p>
		</div>
	</div>
</template>

<script lang="ts" setup>
</script>

<style scoped lang="scss">
$homeNavLengh: 8;
.home-container {
	background-color: white;
	height: 100%;
	flex-grow: 1;
	margin: 10px 0px 0px 10px;
	.home-content {
			width: 100%;
			height: 100%;
			padding: 20px;
			text-align: center;
			h1 {
				font-size: 24px;
				margin-bottom: 10px;
			}
			p {
				font-size: 16px;
			}
		}
}
</style>
