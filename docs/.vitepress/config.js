// .vitepress/config.js
export default {
  // 站点级选项
  base: '/qs-beanfun-5/',
  lang: 'zh-CN',
  title: 'QsBeanfun-5',
  description: '秋水登录器',
  head: [['link', { rel: 'icon', href: 'logo.png' }]],
  lastUpdated: true,
  themeConfig: {
    // 主题级选项
    siteTitle: "",
    nav: [
        { text: 'Blog', link: 'https://tms.mgf8.com/' },
        { text: 'BiliBili', link: 'https://space.bilibili.com/391919722' },
        { text: 'Github', link: 'https://github.com/starmcc/qs-beanfun-5' },
    ],
    footer: {
      message: 'Released under the MIT License. | Q群：童年小梦「资料组」745988842 | Author: 童年小梦 starmcc',
    }
  }
}
