import { GET_HACKABLE_USERS, CHANGE_USER_STATUS } from '../actions/types';

const initialState = {
    users: []
}


export default function(state=initialState, action) {
    switch(action.type){
        case GET_HACKABLE_USERS:
            return {
                ...state,
                users: action.payload
            }
        case CHANGE_USER_STATUS:
            return {
                users: state.users.filter(user => user.pk != action.payload.pk)
            }
        default:
            return {
                ...state
            }
    }
};