import init_data

if __name__ == "__main__":
    init_data.logger.info("Creating initial test data")
    data = init_data.Data(test_mode=True)
    data.create_all()
    init_data.logger.info("Initial test data created")
