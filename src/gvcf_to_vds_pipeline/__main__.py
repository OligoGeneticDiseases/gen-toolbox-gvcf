import sys
import traceback

from gvcf_to_vds_pipeline.cli.command_setup import setup_parser, command_handlers, setup_spark_config

def main():
    """
    Entry point for the application. Parses CLI arguments, sets up Spark/Hail,
    dispatches to the correct handler, and handles global exceptions.
    """
    try:
        parser = setup_parser()
        args = parser.parse_args()

        if args.command is None:
            parser.print_usage()
            sys.exit(1)

        # SparkConf from JSON
        conf = setup_spark_config(args)
        handlers = command_handlers(args, conf)
        command = args.command.lower()

        if command in handlers:
            handlers[command]()
        else:
            print(f"[ERROR] Unknown command: {command}")
            sys.exit(1)

    except AssertionError:
        traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        print("ERROR: " + str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()
