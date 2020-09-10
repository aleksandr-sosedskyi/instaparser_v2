import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles({
    header:{
        backgroundColor: "#333",
        height: "70px",
        '& h5': {
            color: "#fafafa",
            textAlign: "center",
            lineHeight: "35px",
            cursor: "pointer",
            marginBottom: "0"
        }
    },
    tabsDiv: {
        height: "35px",
        backgroundColor: "#777",
        display: "flex",
        justifyContent: "space-around",
        borderTop: "1px solid #fafafa",
        '& p': {
            color: "#fafafa",
            opacity: 1,
            fontSize: "1.1rem",
            lineHeight: "35px",
        }
    },
    mainBlock: {
        height: "calc(100vh - 70px)",
        width: "100vw",
        display: "flex"
    },
    forHack: {
        width: "50vw",
        height: "100%",
    },
    withSecret: {
        width: "50vw",
        height: "100%"
    },
    userEmail: {
        cursor: 'pointer',
        '&:hover': {
            opacity: 0.85
        }
    }
})

export default useStyles;