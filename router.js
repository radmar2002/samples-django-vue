import Vue from 'vue';
import Router from 'vue-router';

import About from '../views/About';
import Home from '../views/Home';
import Login from '../views/Login';
import Lost from '../views/Lost';
import NetworkIssue from '../views/NetworkIssue.vue'
import PasswordReset from '../views/PasswordReset';
import PasswordResetConfirm from '../views/PasswordResetConfirm';
import Register from '../views/Register';
import VerifyEmail from '../views/VerifyEmail';

import Dashboard from '../views/Dashboard.vue';
import Authorboard from '../views/Authorboard.vue';
import Respondentsboard from '../views/respondents/Respondentsboard.vue';

import Playground from '../views/Playground.vue';

import SurveyList from '../views/surveys/SurveyList.vue';
import SurveyDetail from '../views/surveys/SurveyDetail.vue';
import SurveySettings from '../views/surveys/SurveySettings.vue';
import SurveyRespondents from '../views/surveys/SurveyRespondents.vue';
import SurveyPreview from '../views/surveys/SurveyPreview.vue';

import RunningChildSurveyRun from '../views/surveys/RunningChildSurveyRun.vue';

import SurveyCreate from '../views/surveys/SurveyCreate.vue';

import QuestionDetail from '../views/questions/detailsettings/QuestionDetail.vue';
import QuestionDesign from '../views/questions/detailsettings/QuestionDesign.vue';


import SurveyListcards from '@/components/surveys/SurveyListcards.vue';
import SurveyQlist from '@/components/surveys/SurveyQlist.vue';
import ProjectManagement from '@/components/surveys/ProjectManagement.vue';

import ProgressCharts from '@/components/charts/ProgressCharts.vue';

import ListSurveyResults from '@/components/surveyresults/ListSurveyResults.vue';
import QuestionResponsesList from '@/components/surveyresults/QuestionResponsesList.vue';
import QuestionAnalyticsList from '@/components/surveyresults/QuestionAnalyticsList.vue';
import QuestionSimulatorList from '@/components/surveyresults/QuestionSimulatorList.vue';

import ConjointpairsoneCardspreview from '@/views/questions/detailsettings/conjointsettings/ConjointpairsoneCardspreview';


import Projects from '../views/Projects.vue';
import Team from '../views/Team.vue';

import Thankyou from '../views/Thankyou';

import NProgress from 'nprogress'
import store from '../store';


const requireAuthenticated = (to, from, next) => {
  store.dispatch('auth/initialize')
    .then(() => {
      if (!store.getters['auth/isAuthenticated']) {
        next('/login');
      } else {
        next();
      }
    });
  store.dispatch('user/getAccountDetailsAction')
};

const requireUnauthenticated = (to, from, next) => {
  store.dispatch('auth/initialize')
    .then(() => {
      if (store.getters['auth/isAuthenticated']) {
        next('/home');
      } else {
        next();
      }
    });
  store.dispatch('user/forgetUserAction')
};


const redirectLogout = (to, from, next) => {
  store.dispatch('auth/logout')
    .then(() => next('/login'));
};


const beforeEnterSurvey = (routeTo, routeFrom, next) => {
  store.dispatch('auth/initialize')
  store.dispatch('survey/fetchSurveyAction', routeTo.params.id).then(survey => {
    routeTo.params.survey = survey;
    routeTo.params.id = survey.id;
    next()
  }).catch(error => {
    if (error.response && error.response.status == 404) {
      next({
        name: '404',
        params: {
          resource: 'survey'
        }
      })
    } else {
      next({
        name: 'network-issue'
      })
    }
  })
}

const beforeProjectCharts = (routeTo, routeFrom, next) => {
  store.dispatch('auth/initialize')
  store.dispatch('survey/fetchBokehPlotAction').then(dataPlot => {
    routeTo.params.plot = dataPlot;
    next()
  }).catch(error => {
    if (error.response && error.response.status == 404) {
      next({
        name: '404',
        params: {
          resource: 'survey'
        }
      })
    } else {
      next({
        name: 'network-issue'
      })
    }
  })
}

const beforeEnterRunningChildSurvey = (routeTo, routeFrom, next) => {
  store.dispatch('auth/initialize')
  store.dispatch('survey/accessPublicSurveyAction', {
    survey_token: routeTo.params.token,
    parent_survey_id: routeTo.params.id
  }).then(survey => {
    routeTo.params.survey = survey;
    routeTo.params.id = survey.id;
    next()
  }).catch(error => {
    if (error.response && error.response.status == 404) {
      next({
        name: '404',
        params: {
          resource: 'survey'
        }
      })
    } else {
      next({
        name: 'network-issue'
      })
    }
  })
}

const beforeEnterSurveyRespondents = (routeTo, routeFrom, next) => {
  store.dispatch('auth/initialize')
  store.dispatch('respondents/fetchAllSurveyRespondentsAction', {
    parentsurvey_id: routeTo.params.id
  })
  store.dispatch('survey/fetchSurveyAction', routeTo.params.id).then(survey => {
    routeTo.params.survey = survey;
    routeTo.params.id = survey.id;
    next()
  }).catch(error => {
    if (error.response && error.response.status == 404) {
      next({
        name: '404',
        params: {
          resource: 'survey'
        }
      })
    } else {
      next({
        name: 'network-issue'
      })
    }
  })
}

const beforeEnterAuthorboard = (routeTo, routeFrom, next) => {
  store.dispatch('auth/initialize')
  store.dispatch('survey/fetchAllsurveysAction').then(() => {
    next()
  }).catch(error => {
    if (error.response && error.response.status == 404) {
      next({
        name: '404',
        params: {
          resource: 'surveys'
        }
      })
    } else {
      next({
        name: 'network-issue'
      })
    }
  })
}

const beforeEnterRespondents = (routeTo, routeFrom, next) => {
  store.dispatch('auth/initialize')
  store.dispatch('respondents/fetchAllrespondentsAction').then(() => {
    next()
  }).catch(error => {
    if (error.response && error.response.status == 404) {
      next({
        name: '404',
        params: {
          resource: 'respondents'
        }
      })
    } else {
      next({
        name: 'network-issue'
      })
    }
  })
}

const beforeEnterSurveyList = (routeTo, routeFrom, next) => {
  store.dispatch('auth/initialize')
  store.dispatch('survey/fetchSurveysAction').then(() => {
    next()
  }).catch(error => {
    if (error.response && error.response.status == 404) {
      next({
        name: '404',
        params: {
          resource: 'respondents'
        }
      })
    } else {
      next({
        name: 'network-issue'
      })
    }
  })
}

const beforeEnterQuestion = (routeTo, routeFrom, next) => {
  store.dispatch('auth/initialize')
  store.dispatch('survey/fetchSurveyAction', routeTo.params.id).then(survey => {
    routeTo.params.survey = survey;
    routeTo.params.id = survey.id;
    next()
  })
  store.dispatch('survey/fetchQuestionAction', {
    surveyId: routeTo.params.id,
    questionId: routeTo.params.q_id
  }).then(question => {
    routeTo.params.question = question;
    routeTo.params.id = question.survey;
    routeTo.params.q_id = question.id;
    next()
  }).catch(error => {
    if (error.response && error.response.status == 404) {
      next({
        name: '404',
        params: {
          resource: 'question'
        }
      })
    } else {
      next({
        name: 'network-issue'
      })
    }
  })
}


Vue.use(Router);

//const parseProps = r => ({ id:parseInt(r.params.id), q_id:parseInt(r.params.q_id) });

const router = new Router({
  saveScrollPosition: true,
  mode: 'history',
  routes: [{
      path: '/about',
      component: About,
      beforeEnter: requireAuthenticated,
    },
    {
      path: '/',
      component: Home,
      beforeEnter: requireAuthenticated,
    },
    {
      path: '/playground',
      component: Playground,
      beforeEnter: requireAuthenticated
    },
    {
      path: '/password_reset',
      component: PasswordReset,
    },
    {
      path: '/password_reset/:uid/:token',
      component: PasswordResetConfirm,
    },
    {
      path: '/register',
      name: 'register',
      component: Register,
    },
    {
      path: '/register/:key',
      component: VerifyEmail,
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
      beforeEnter: requireUnauthenticated,
    },
    {
      path: '/thankyou',
      name: 'thankyou',
      component: Thankyou,
      props: true,
      //beforeEnter: requireUnauthenticated,
    },
    {
      path: '/logout',
      name: 'logout',
      beforeEnter: redirectLogout,
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: Dashboard,
      beforeEnter: requireAuthenticated,
    },
    {
      path: '/authorboard',
      name: 'authorboard',
      props: true,
      component: Authorboard,
      beforeEnter: beforeEnterAuthorboard,
    },
    {
      path: '/respondents',
      name: 'respondents',
      props: true,
      component: Respondentsboard,
      beforeEnter: beforeEnterRespondents,
    },
    {
      path: '/listcards',
      name: 'listcards',
      component: SurveyListcards,
      beforeEnter: requireAuthenticated,
    },
    {
      path: '/surveyqlist',
      name: 'surveyqlist',
      component: SurveyQlist,
      beforeEnter: beforeEnterAuthorboard,
    },
    {
      path: '/projectmanagement',
      name: 'projectmanagement',
      component: ProjectManagement,
      beforeEnter: requireAuthenticated,
    },
    {
      path: '/progresscharts',
      name: 'progresscharts',
      component: ProgressCharts,
      props: true,
      beforeEnter: beforeProjectCharts,
    },
    {
      path: '/survey-list',
      name: 'survey-list',
      component: SurveyList,
      props: true,
      beforeEnter: beforeEnterSurveyList
    },
    {
      path: '/survey-create',
      name: 'survey-create',
      component: SurveyCreate,
      beforeEnter: requireAuthenticated
    },
    {
      path: '/survey-detail/:id',
      name: 'survey-detail',
      props: true,
      //props: parseProps,
      component: SurveyDetail,
      beforeEnter: beforeEnterSurvey,
    },
    {
      path: '/survey-results-list/:id',
      name: 'survey-results-list',
      props: true,
      //props: parseProps,
      component: ListSurveyResults,
      beforeEnter: beforeEnterSurvey,
    },
    {
      path: '/survey-results-list/:id/question-responses-list/:q_id',
      name: 'question-responses-list',
      props: true,
      //props: parseProps,
      component: QuestionResponsesList,
      //component: mapEditQuestionComponent('EMOTION'),
      beforeEnter: beforeEnterQuestion,
    },
    {
      path: '/survey-results-list/:id/question-simulator-list/:q_id',
      name: 'question-simulator-list',
      props: true,
      //props: parseProps,
      component: QuestionSimulatorList,
      //component: mapEditQuestionComponent('EMOTION'),
      beforeEnter: beforeEnterQuestion,
    },
    {
      path: '/survey-results-list/:id/question-analytics-list/:q_id',
      name: 'question-analytics-list',
      props: true,
      //props: parseProps,
      component: QuestionAnalyticsList,
      //component: mapEditQuestionComponent('EMOTION'),
      beforeEnter: beforeEnterQuestion,
    },
    {
      path: '/survey-settings/:id',
      name: 'survey-settings',
      props: true,
      //props: parseProps,
      component: SurveySettings,
      beforeEnter: beforeEnterSurvey,
    },
    {
      path: '/survey-respondents/:id',
      name: 'survey-respondents',
      props: true,
      //props: parseProps,
      component: SurveyRespondents,
      beforeEnter: beforeEnterSurveyRespondents,
    },
    {
      path: '/survey-preview/:id',
      name: 'survey-preview',
      props: true,
      //props: parseProps,
      component: SurveyPreview,
      beforeEnter: beforeEnterSurvey,
    },
    {
      path: '/shared-survey-run/:token/:id',
      name: 'shared-survey-run',
      props: true,
      //props: parseProps,
      component: RunningChildSurveyRun,
      beforeEnter: beforeEnterRunningChildSurvey,
      meta: {
        header: 'public'
      },
    },
    {
      path: '/survey-detail/:id/question-detail/:q_id',
      name: 'question-detail',
      props: true,
      //props: parseProps,
      component: QuestionDetail,
      //component: mapEditQuestionComponent('EMOTION'),
      beforeEnter: beforeEnterQuestion,
    },
    {
      path: '/survey-detail/:id/question-design/:q_id',
      name: 'question-design',
      props: true,
      //props: parseProps,
      component: QuestionDesign,
      beforeEnter: beforeEnterQuestion,
    },
    {
      path: '/survey-detail/:id/question-cardsonepreview/:q_id',
      name: 'question-cardsonepreview',
      props: true,
      //props: parseProps,
      component: ConjointpairsoneCardspreview,
      beforeEnter: beforeEnterQuestion,
    },
    {
      path: '/projects',
      name: 'projects',
      component: Projects,
      beforeEnter: requireAuthenticated,
    },
    {
      path: '/team',
      name: 'team',
      component: Team,
      beforeEnter: requireAuthenticated,
    },
    {
      path: '/404',
      name: '404',
      component: Lost,
      props: true // I added this so we can receive the param as a prop
    },
    {
      path: '/network-issue',
      name: 'network-issue',
      component: NetworkIssue
    },
    {
      path: '*',
      redirect: {
        name: '404',
        params: {
          resource: 'page'
        }
      } // I added this resource param here.
    },
  ],
});


router.beforeEach((routeTo, routeFrom, next) => {
  NProgress.start()
  next()
});

router.afterEach(() => {
  NProgress.done()
});

export default router