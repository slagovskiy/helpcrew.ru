import Vue from 'vue'

import './styles/quasar.styl'
import '@quasar/extras/roboto-font/roboto-font.css'
import '@quasar/extras/material-icons/material-icons.css'
import '@quasar/extras/fontawesome-v5/fontawesome-v5.css'
import {
    Quasar,
    QLayout,
    QHeader,
    QDrawer,
    QPageContainer,
    QPage,
    QToolbar,
    QToolbarTitle,
    QForm,
    QBtn,
    QIcon,
    QInput,
    QList,
    QItem,
    QItemSection,
    QItemLabel,
    QCard,
    QCardSection,
    QCardActions,
    QSeparator,
    QSpace,
} from 'quasar'

Vue.use(Quasar, {
    config: {},
    components: {
        QLayout,
        QHeader,
        QDrawer,
        QPageContainer,
        QPage,
        QToolbar,
        QToolbarTitle,
        QForm,
        QBtn,
        QIcon,
        QInput,
        QList,
        QItem,
        QItemSection,
        QItemLabel,
        QCard,
        QCardSection,
        QCardActions,
        QSeparator,
        QSpace,
    },
    directives: {},
    plugins: {}
})