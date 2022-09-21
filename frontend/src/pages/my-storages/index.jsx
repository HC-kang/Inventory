import React, { useEffect, useState } from "react";
import FastAPIClient from "../../client";
import config from "../../config";
import DashboardHeader from "../../components/DashboardHeader";
import Footer from "../../components/Footer";
import jwtDecode from "jwt-decode";
import * as moment from "moment";
import StorageTable from "../../components/StorageTable";
import FormInput from "../../components/FormInput/FormInput";
import Button from "../../components/Button/Button";
import { NotLoggedIn } from "./NotLoggedIn";
import Loader from "../../components/Loader";
import PopupModal from "../../components/Modal/PopupModal";

const client = new FastAPIClient(config);

const ProfileView = ({ storages }) => {
	return (
		<>
			<StorageTable
				storages={storages}
				
				showUpdate={true}
			/>
			
		</>
	);
};

const StorageDashboard = () => {
	const [isLoggedIn, setIsLoggedIn] = useState(false);
	const [error, setError] = useState({ label: "", url: "", source: "" });
	const [storageForm, setStorageForm] = useState({
		label: "",
		url: "https://",
		source: "",
	});

	const [showForm, setShowForm] = useState(false);
	const [storages, setStorages] = useState([]);

	const [loading, setLoading] = useState(false);
	const [refreshing, setRefreshing] = useState(true);

	useEffect(() => {
		fetchUserStorages();
	}, []);

	const fetchUserStorages = () => {
		client.getUserStorages().then((data) => {
			setRefreshing(false);
			setStorages(data?.results);
		});
	};

   const urlPatternValidation = URL => {
        const regex = new RegExp('(https?://)?([\\da-z.-]+)\\.([a-z.]{2,6})[/\\w .-]*/?');
          return regex.test(URL);
        };

	const onCreateStorage = (e) => {
		e.preventDefault();
		setLoading(true);
		setError(false);

		if (storageForm.label.length <= 0) {
			setLoading(false);
			return setError({ label: "Please Enter Storage Label" });
		}
		if (storageForm.url.length <= 0) {
			setLoading(false);
			return setError({ url: "Please Enter Storage Url" });
		}
		if (!urlPatternValidation(storageForm.url)) {
			setLoading(false);
			return setError({ url: "Please Enter Valid URL" });
		}
		if (storageForm.source.length <= 0) {
			setLoading(false);
			return setError({ source: "Please Enter Storage Source" });
		}

		client.fetchUser().then((user) => {
			client
				.createStorage(
					storageForm.label,
					storageForm.url,
					storageForm.source,
					user?.id
				)
				// eslint-disable-next-line no-unused-vars
				.then((data) => {  // eslint:ignore
					fetchUserStorages();
					setLoading(false);
					setShowForm(false);
				});
		});
	};

	useEffect(() => {
		const tokenString = localStorage.getItem("token");
		if (tokenString) {
			const token = JSON.parse(tokenString);
			const decodedAccessToken = jwtDecode(token.access_token);
			if (moment.unix(decodedAccessToken.exp).toDate() > new Date()) {
				setIsLoggedIn(true);
			}
		}
	}, []);

	if (refreshing) return !isLoggedIn ? <NotLoggedIn /> : <Loader />;

	return (
		<>
			<section
				className="flex flex-col bg-black text-center"
				style={{ minHeight: "100vh" }}
			>
				<DashboardHeader />
				<div className="container px-5 pt-6 text-center mx-auto lg:px-20">
						{/*TODO - move to component*/}
					<h1 className="mb-12 text-3xl font-medium text-white">
						Storages - Better than all the REST
					</h1>

					<button
						className="my-5 text-white bg-teal-500 p-3 rounded"
						onClick={() => {
							setShowForm(!showForm);
						}}
					>
						Create Storage
					</button>

					<p className="text-base leading-relaxed text-white">Latest storages</p>
					<div className="mainViewport text-white">
						{storages.length && (
							<ProfileView
								storages={storages}
								fetchUserStorages={fetchUserStorages}
							/>
						)}
					</div>
				</div>

				<Footer />
			</section>
			{showForm && (
				<PopupModal
					modalTitle={"Create Storage"}
					onCloseBtnPress={() => {
						setShowForm(false);
						setError({ fullName: "", email: "", password: "" });
					}}
				>
					<div className="mt-4 text-left">
						<form className="mt-5" onSubmit={(e) => onCreateStorage(e)}>
							<FormInput
								type={"text"}
								name={"label"}
								label={"Label"}
								error={error.label}
								value={storageForm.label}
								onChange={(e) =>
									setStorageForm({ ...storageForm, label: e.target.value })
								}
							/>
							<FormInput
								type={"text"}
								name={"url"}
								label={"Url"}
								error={error.url}
								value={storageForm.url}
								onChange={(e) =>
									setStorageForm({ ...storageForm, url: e.target.value })
								}
							/>
							<FormInput
								type={"text"}
								name={"source"}
								label={"Source"}
								error={error.source}
								value={storageForm.source}
								onChange={(e) =>
									setStorageForm({ ...storageForm, source: e.target.value })
								}
							/>
							<Button
								loading={loading}
								error={error.source}
								title={"Create Storage"}
							/>
						</form>
					</div>
				</PopupModal>
			)}
		</>
	);
};

export default StorageDashboard;
