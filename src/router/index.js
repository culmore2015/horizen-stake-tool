import Vue from 'vue';
import Router from 'vue-router';

Vue.use(Router);

export default new Router({
    routes: [
        {
            path: '/',
            redirect: '/list'
        },
        {
            path: '/',
            component: () => import(/* webpackChunkName: "home" */ '../components/common/Home.vue'),
            meta: { title: '自述文件' },
            children: [
                {
                    path: '/list',
                    component: () => import(/* webpackChunkName: "stakelist" */ '../components/page/StakeList.vue'),
                    meta: { title: '验证列表' }
                },
                {
                    path: '/create',
                    component: () => import(/* webpackChunkName: "createstake" */ '../components/page/CreateStake.vue'),
                    meta: { title: '添加绑定' }
                },
                {
                    path: '/verify',
                    component: () => import(/* webpackChunkName: "verifystake" */ '../components/page/VerifyStake.vue'),
                    meta: { title: '验证绑定' }
                },
                {
                    path: '/404',
                    component: () => import(/* webpackChunkName: "404" */ '../components/page/404.vue'),
                    meta: { title: '404' }
                },
                {
                    path: '/403',
                    component: () => import(/* webpackChunkName: "403" */ '../components/page/403.vue'),
                    meta: { title: '403' }
                }
            ]
        },
        {
            path: '/login',
            component: () => import(/* webpackChunkName: "login" */ '../components/page/Login.vue'),
            meta: { title: '登录' }
        },
        {
            path: '*',
            redirect: '/404'
        }
    ]
});
