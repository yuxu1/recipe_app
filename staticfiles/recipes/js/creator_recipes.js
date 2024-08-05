const modal = document.querySelector("[data-modal]")
const openButton = document.querySelector("[data-open-modal]")
const closeButton = document.querySelector("[data-close-modal]")
openButton.addEventListener("click", () => {
    modal.showModal()
})
closeButton.addEventListener("click", () => {
    modal.close()
})