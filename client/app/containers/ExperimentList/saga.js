import { put, takeLatest, select } from 'redux-saga/effects';
import ModelchimpClient from 'utils/modelchimpClient';
import { LOAD_EXPERIMENT_DATA } from './constants';
import {
  loadExperimentSuccessAction,
  loadExperimentErrorAction,
} from './actions';
import {
  makeSelectExperimentColumns,
  makeSelectExperimentMetricColumns,
} from './selectors';

export function* getExperimentList({ projectId }) {
  let requestURL = `ml-model/${projectId}/`;
  let cols = yield select(makeSelectExperimentColumns());
  let metricCols = yield select(makeSelectExperimentMetricColumns());

  if ((cols && cols.length > 0) || (metricCols && metricCols.length > 0)) {
    cols = cols.map(e => `param_fields[]=${e}&`);
    cols = cols.join('');
    metricCols = metricCols.map(e => `metric_fields[]=${e}&`);
    metricCols = metricCols.join('');

    requestURL = `${requestURL}?${cols}${metricCols}`;
  }

  try {
    const experiments = yield ModelchimpClient.get(requestURL);

    yield put(loadExperimentSuccessAction(experiments));
  } catch (err) {
    yield put(loadExperimentErrorAction(err));
  }
}

export default function* experimentListSaga() {
  yield takeLatest(LOAD_EXPERIMENT_DATA, getExperimentList);
}
