import Storage from "../Storage";
import React, {useState} from "react";
import PopupModal from "../Modal/PopupModal";
import FormInput from "../FormInput/FormInput";

const StorageTable = ({storages}) => {

  const [storageInfoModal, setStorageInfoModal] = useState(false)

    return (
      <>
        <div className="sections-list">
          {storages.length && (
              storages.map((storage) => (
                <Storage showStorageInfoModal={() => setStorageInfoModal(storage)} key={storage.id} storage={storage}  />
              ))
          )}
          {!storages.length && (
              <p>No storages found!</p>
          )}
        </div>
        {storageInfoModal && <PopupModal
						modalTitle={"Storage Info"}
						onCloseBtnPress={() => {
							setStorageInfoModal(false);
						}}
					>
						<div className="mt-4 text-left">
							<div>hi</div>
							<form className="mt-5">
								<FormInput
									disabled
									type={"text"}
									name={"label"}
									label={"Label"}
									value={storageInfoModal?.name}
								/>
								<FormInput
									disabled
									type={"text"}
									name={"url"}
									label={"Url"}
									value={storageInfoModal?.name}
								/>
								<FormInput
									disabled
									type={"text"}
									name={"source"}
									label={"Source"}
									value={storageInfoModal?.name}
								/>
							</form>
						</div>
					</PopupModal>}
      </>
    )
}

export default StorageTable;