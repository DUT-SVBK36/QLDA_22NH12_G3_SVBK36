import { StyleSheet } from "react-native";
import { BaseColors } from "@/constants/Colors";

const styles = StyleSheet.create({
  modalOverlay: {
    flex: 1,
    backgroundColor: "rgba(0, 0, 0, 0.7)",
    justifyContent: "center",
    alignItems: "center",
  },
  modalContent: {
    backgroundColor: BaseColors.white,
    borderRadius: 12,
    width: "85%",
    padding: 20,
    alignItems: "center",
    shadowColor: "#000",
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  title: {
    color: BaseColors.primary,
    marginBottom: 16,
    // fontWeight: "bold",
    textAlign: "center",
  },
  imageContainer: {
    width: "100%",
    aspectRatio: 1,
    borderRadius: 8,
    overflow: "hidden",
    marginBottom: 16,
  },
  image: {
    width: "100%",
    height: "100%",
  },
  infoContainer: {
    width: "100%",
    marginBottom: 20,
  },
  infoText: {
    color: BaseColors.black,
    marginBottom: 8,
  },
  recommendation: {
    color: BaseColors.black,
    marginTop: 8,
    fontStyle: "italic",
  },
  button: {
    backgroundColor: BaseColors.primary,
    paddingVertical: 12,
    paddingHorizontal: 30,
    borderRadius: 8,
    alignSelf: "center",
  },
  buttonText: {
    color: BaseColors.white,
    fontWeight: "bold",
    fontSize: 16,
  },
});

export default styles;
