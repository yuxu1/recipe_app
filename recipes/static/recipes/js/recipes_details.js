const updateModal = document.querySelector("[data-modal]")
const openUpdateButton = document.querySelector("[data-open-modal]")
const closeUpdateButton = document.querySelector("[data-close-modal]")
const deleteModal = document.querySelector("[delete-modal]")
const openDeleteButton = document.querySelector("[open-delete-modal]")
const closeDeleteButton = document.querySelector("[close-delete-modal]")

//open update modal
openUpdateButton.addEventListener("click", () => {
    updateModal.showModal()
})
//close update modal
closeUpdateButton.addEventListener("click", () => {
    updateModal.close()
})
//open delete modal
openDeleteButton.addEventListener("click", () => {
    deleteModal.showModal()
})
//close delete modal
closeDeleteButton.addEventListener("click", () => {
    deleteModal.close()
})